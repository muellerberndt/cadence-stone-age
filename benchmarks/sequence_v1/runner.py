"""Run the sequence instrument: training lives, frozen evaluations and the withdrawal branch.

One founder brain is composed per seed and recipe; every training arm starts from a copy of
it. A life runs whole episodes on one continuing brain. The last executed action's outcome is
held at a seam with the checkpoint (``seam.json``), never delivered with an observation whose
action would then be thrown away. Frozen evaluations read copies of a checkpoint with their own
action-sampling stream; the living brain is never evaluated in place.

    python runner.py --protocol protocol.json --out OUT --seeds 1001 --arms natural_step
    python runner.py --report OUT
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from adapters import ADAPTERS, PendingOutcome, readout  # noqa: E402
from metrics import (  # noqa: E402
    chain_success,
    episode_summary,
    paired_bootstrap,
    uniform_chain_success_exact,
)
from probes import Copier, reseed_actions, state_digest  # noqa: E402
from receipts import Manifest, canonical  # noqa: E402
from worlds import action_id, balanced_routes, make_world, recall_schedule  # noqa: E402

SCHEMA = "stone-age-sequence/1"
CONTROLS = ("founder", "random", "oracle")
STREAM = {"evaluation": 1, "random": 2, "routes": 3, "withdrawal_routes": 4}


def load_protocol(path: Path) -> tuple[dict[str, Any], str]:
    raw = Path(path).read_bytes()
    protocol = json.loads(raw)
    if protocol.get("schema") != SCHEMA:
        raise ValueError(f"protocol schema must be {SCHEMA}")
    for name, arm in protocol["arms"].items():
        if arm["adapter"] not in ADAPTERS:
            raise ValueError(f"arm {name}: unknown adapter {arm['adapter']!r}")
        if arm["caregiver"] not in ("none", "grade", "correct", "guide"):
            raise ValueError(f"arm {name}: unknown caregiver {arm['caregiver']!r}")
        if arm["adapter"] == "live" and arm["caregiver"] in ("correct", "guide"):
            raise ValueError(f"arm {name}: live takes no teacher; declare an ordering first")
    return protocol, hashlib.sha256(raw).hexdigest()


def stream_seed(*parts: int) -> int:
    """A deterministic seed for one named random stream of one founder."""
    return int(np.random.SeedSequence([int(p) for p in parts]).generate_state(1)[0])


def observation_digest(x: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(x, dtype=np.float64).tobytes()).hexdigest()[:16]


# -- brains


def compose(recipe: dict[str, Any], seed: int, world: dict[str, Any], extra: dict[str, Any]) -> Any:
    from cadence import Brain  # noqa: PLC0415

    options = dict(recipe.get("compose", {}))
    options.update(extra)
    if "modules" in options:
        options["modules"] = tuple(int(width) for width in options["modules"])
    probe = make_world(world, route=0)
    return Brain.compose(inputs=probe.inputs, actions=probe.actions, seed=int(seed), **options)


def describe(brain: Any) -> dict[str, Any]:
    def plain(value: Any) -> Any:
        if isinstance(value, dict):
            return {str(k): plain(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [plain(v) for v in value]
        if isinstance(value, (np.floating, np.integer)):
            return value.item()
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return repr(value)

    return plain(brain.describe())


# -- caregiver


@dataclass(frozen=True)
class Caregiver:
    """V5's caregiver: windows of ``guided`` decisions alternate with ``autonomous`` ones,
    counted in executed decisions of the whole life. ``grade`` adds +right/-wrong to the
    world's reward of the executed action in guided windows; ``correct`` labels the current
    observation with its required action after an executed nonterminal mistake in a guided
    window; ``guide`` labels every decision's observation in a guided window with its required
    action before the brain acts (uniform current-state teaching, which also reaches a decision
    whose mistake ends the episode). Labels and grades come from the world's scorer, never from
    the brain's input."""

    kind: str
    guided_span: int
    autonomous_span: int
    right: float = 0.5
    wrong: float = -0.5

    def guided(self, decision: int) -> bool:
        cycle = self.guided_span + self.autonomous_span
        if self.kind == "none" or self.guided_span <= 0 or cycle <= 0:
            return False
        return decision % cycle < self.guided_span

    def grade(self, guided: bool, outcome: Any) -> float:
        if self.kind != "grade" or not guided or not outcome.decision or outcome.required is None:
            return 0.0
        return self.right if outcome.advanced else self.wrong

    def label(self, guided: bool, outcome: Any, world: Any, next_guided: bool = False) -> int | None:
        if self.kind == "guide":
            # the observation shown next, if its decision falls in a guided window
            return world.required() if next_guided and not world.done else None
        if self.kind != "correct" or not guided or not outcome.decision:
            return None
        if outcome.advanced or outcome.done:
            return None
        return world.required()


# -- lives


@dataclass
class Life:
    events: list[dict[str, Any]]
    seam: PendingOutcome
    episodes: list[dict[str, Any]]
    counts: dict[str, Any]


def run_life(
    adapter: Any,
    world_spec: dict[str, Any],
    caregiver: Caregiver,
    episodes: int,
    *,
    life_id: str,
    routes: list[int] | None = None,
    seam: PendingOutcome | None = None,
) -> Life:
    """``episodes`` whole episodes on one continuing brain. A life that starts from a seam
    delivers the held outcome with its first observation, exactly once."""
    if episodes < 1:
        raise ValueError("a life runs at least one episode")
    events: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    teaching = {"labels": 0, "refused": 0, "exhausted": 0}
    decision = 0
    episode = 0

    def new_world(index: int) -> Any:
        return make_world(world_spec, None if routes is None else routes[index])

    world = new_world(0)
    x = world.observation()
    if seam is None:
        action, choice = adapter.first(x)
        choice.pop("learning", None)  # nothing was learned before a life's first action
    else:
        action, choice = adapter.resume(seam, x)
        resumed = choice.pop("learning", {})
    episode_decisions = 0
    resumed_learning = resumed if seam is not None else None
    while True:
        guided = caregiver.guided(decision)
        stage_before = world.stage
        outcome = world.step(action)
        grade = caregiver.grade(guided, outcome)
        consumed = outcome.reward + grade
        event = {
            "life": life_id,
            "episode": episode,
            "decision": decision if outcome.decision else None,
            "kind": "decision" if outcome.decision else "observe",
            "observation": observation_digest(x),
            "stage_before": stage_before,
            "required": outcome.required,
            "action": action,
            "choice": choice,
            "advanced": outcome.advanced,
            "reason": outcome.reason,
            "world_reward": outcome.reward,
            "grade": grade,
            "consumed_reward": consumed,
            "done": outcome.done,
            "success": outcome.success,
            "guided": guided,
            "label": None,
        }
        if outcome.decision:
            decision += 1
            episode_decisions += 1
        if outcome.done:
            summaries.append(
                {
                    "episode": episode,
                    "success": outcome.success,
                    "decisions": episode_decisions,
                    "stage_reached": world.stage,
                    "reason": outcome.reason,
                }
            )
        if outcome.done and episode == episodes - 1:
            held = adapter.hold(consumed, True)
            event["held"] = held.to_dict()
            event["learning"] = {}  # owed at the seam: nothing was learned from it yet
            events.append(event)
            break
        if outcome.done:
            episode += 1
            episode_decisions = 0
            world = new_world(episode)
            label = caregiver.label(guided, outcome, world, caregiver.guided(decision)) if caregiver.kind == "guide" else None
        else:
            label = caregiver.label(guided, outcome, world, caregiver.guided(decision))
        x = world.observation()
        action, record = adapter.next(x, reward=consumed, done=outcome.done, teacher=label)
        event["label"] = label
        learning = record.pop("learning", {})
        event["learning"] = learning
        if label is not None:
            teaching["labels"] += 1
            if not learning.get("demonstration_accepted", learning.get("demonstrations", 0.0)):
                teaching["refused"] += 1
            if learning.get("demonstration_free_budget_exhausted", 0.0) > 0:
                teaching["exhausted"] += 1
            teaching["sweeps"] = teaching.get("sweeps", 0) + int(
                learning.get("demonstration_total_row_sweeps", 0)
            )
        choice = record
        events.append(event)
    counts = {
        "resumed_learning": resumed_learning,
        "decisions": decision,
        "events": len(events),
        "episodes": len(summaries),
        "teaching": teaching,
        "refusals": adapter.refusals,
        "teaching_refusals": adapter.teaching_refusals,
        "outcomes_delivered": len(adapter.ledger.consumed),
        "actions_issued": adapter.ledger.issued,
    }
    return Life(events, held, summaries, counts)


# -- frozen evaluation


def evaluate(
    checkpoint: Path,
    world_spec: dict[str, Any],
    *,
    episodes: int,
    greedy: bool,
    seed: int,
    reset: str = "episode",
    routes: list[int] | None = None,
) -> list[dict[str, Any]]:
    """Frozen reading of a checkpoint copy: ``act`` only, so no parameter or store changes;
    the working trace and settled activity still move within an episode."""
    from cadence import Brain  # noqa: PLC0415

    if reset not in ("episode", "continuing"):
        raise ValueError("reset is 'episode' or 'continuing'")
    brain = Brain.load(checkpoint)
    reseed_actions(brain, seed)
    rows = []
    for index in range(episodes):
        if reset == "episode" or index == 0:
            brain.reset()
        world = make_world(world_spec, None if routes is None else routes[index])
        undecided = refusals = 0
        first_choice = None
        while not world.done:
            x = world.observation()
            try:
                out = brain.act(x, greedy=greedy)
            except RuntimeError:
                refusals += 1
                break
            action = action_id(out, world.actions)
            reading = readout(brain)
            undecided += int(reading.get("undecided", False))
            outcome = world.step(action)
            if outcome.decision and first_choice is None:
                first_choice = {"action": action, "required": outcome.required}
        rows.append(
            {
                "episode": index,
                "route": None if routes is None else routes[index],
                "success": bool(world.success) and refusals == 0,
                "decisions": world.decisions,
                "stage_reached": world.stage,
                "reason": "refused" if refusals else ("success" if world.success else _reason(world)),
                "refusals": refusals,
                "undecided": undecided,
                "first_choice": first_choice,
            }
        )
    return rows


def _reason(world: Any) -> str:
    return "locked" if getattr(world, "locked", False) else "timeout"


def control_rows(kind: str, world_spec: dict[str, Any], *, episodes: int, seed: int,
                 routes: list[int] | None = None) -> list[dict[str, Any]]:
    """Uniform random over the alphabet, or the stage-aware oracle that reads the scorer
    (a scorer sanity check, never a Cadence answer path)."""
    rng = np.random.default_rng(seed)
    rows = []
    for index in range(episodes):
        world = make_world(world_spec, None if routes is None else routes[index])
        while not world.done:
            if kind == "random":
                action = int(rng.integers(world.actions))
            else:
                required = world.required()
                # no decision is due: any valid action, the world ignores it
                action = 0 if required is None else int(required)
            world.step(action)
        rows.append(
            {
                "episode": index,
                "route": None if routes is None else routes[index],
                "success": bool(world.success),
                "decisions": world.decisions,
                "stage_reached": world.stage,
                "reason": "success" if world.success else _reason(world),
            }
        )
    return rows


# -- one founder


def write_jsonl_gz(path: Path, rows: list[dict[str, Any]]) -> str:
    with open(path, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as handle:
        for row in rows:
            handle.write(canonical(row) + b"\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    names = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=names)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in row.items()})


def run_founder(protocol: dict[str, Any], seed: int, arms: list[str], recipe_name: str,
                out: Path) -> dict[str, Any]:
    from cadence import Brain  # noqa: PLC0415

    world = protocol["world"]
    schedule = protocol["schedule"]
    evaluation = protocol["evaluation"]
    recipe = protocol["recipes"][recipe_name]
    directory = out / recipe_name / f"founder-{seed}"
    directory.mkdir(parents=True, exist_ok=True)
    copier = Copier(directory / "copies")
    founder_path = directory / "founder.npz"
    founder = compose(recipe, seed, world, {})
    founder.save(founder_path)
    result: dict[str, Any] = {
        "seed": seed,
        "recipe": recipe_name,
        "genes": describe(founder),
        "founder_digest": state_digest(founder, copier),
        "arms": {},
    }
    needs_routes = world["kind"] in ("route_cue", "recall")
    schedule_of = recall_schedule if world["kind"] == "recall" else balanced_routes
    train_routes = (
        schedule_of(protocol["training_episodes"], np.random.default_rng(stream_seed(STREAM["routes"], seed)))
        if needs_routes else None
    )
    after_routes = (
        schedule_of(protocol["withdrawal_episodes"], np.random.default_rng(stream_seed(STREAM["withdrawal_routes"], seed)))
        if needs_routes and protocol.get("withdrawal_episodes", 0) > 0 else None
    )
    eval_routes = (
        schedule_of(evaluation["episodes"], np.random.default_rng(stream_seed(STREAM["routes"], seed, 1)))
        if needs_routes else None
    )

    def frozen(checkpoint: Path) -> dict[str, Any]:
        readings = {}
        for mode in evaluation["modes"]:
            rows = evaluate(
                checkpoint, world, episodes=evaluation["episodes"], greedy=mode == "greedy",
                seed=stream_seed(STREAM["evaluation"], seed, 0 if mode == "greedy" else 1),
                reset=evaluation.get("reset", "episode"), routes=eval_routes,
            )
            readings[mode] = {"summary": episode_summary(rows, make_world(world, route=0).stages), "rows": rows}
        return readings

    result["arms"]["founder"] = {"frozen": frozen(founder_path)}
    for kind in ("random", "oracle"):
        rows = control_rows(kind, world, episodes=evaluation["episodes"],
                            seed=stream_seed(STREAM["random"], seed), routes=eval_routes)
        result["arms"][kind] = {"frozen": {"sampled": {"summary": episode_summary(rows, make_world(world, route=0).stages), "rows": rows}}}

    for arm in arms:
        spec = protocol["arms"][arm]
        started = time.time()
        brain = Brain.load(founder_path)
        if spec.get("compose"):
            brain = compose(recipe, seed, world, spec["compose"])  # a different numerical arm: recompose
            if state_digest(brain, copier) == result["founder_digest"]:
                raise RuntimeError(f"arm {arm}: its compose override changed nothing")
            parent = Brain.load(founder_path)
            if not (
                np.array_equal(brain.brain.efficacy, parent.brain.efficacy)
                and np.array_equal(brain.brain.bias, parent.brain.bias)
            ):
                raise RuntimeError(f"arm {arm}: its override changed the founder's initial weights")
        adapter = ADAPTERS[spec["adapter"]](brain, make_world(world, route=0).actions)
        caregiver = Caregiver(spec["caregiver"], schedule["guided"], schedule["autonomous"])
        life = run_life(adapter, world, caregiver, protocol["training_episodes"],
                        life_id=f"{recipe_name}/{seed}/{arm}/train", routes=train_routes)
        trained = directory / f"{arm}-trained.npz"
        brain.save(trained)
        (directory / f"{arm}-trained.seam.json").write_text(json.dumps(life.seam.to_dict()))
        arm_result: dict[str, Any] = {
            "spec": spec,
            "training": {"counts": life.counts, "summary": episode_summary(life.episodes, make_world(world, route=0).stages)},
            "trained_digest": state_digest(brain, copier),
            "events_sha256": write_jsonl_gz(directory / f"{arm}-train-events.jsonl.gz", life.events),
            "frozen": frozen(trained),
        }
        if protocol.get("withdrawal_episodes", 0) > 0:
            living = Brain.load(trained)
            seam = PendingOutcome(**json.loads((directory / f"{arm}-trained.seam.json").read_text()))
            follow = ADAPTERS[spec["adapter"]](living, make_world(world, route=0).actions)
            after = run_life(follow, world, Caregiver("none", 0, 1), protocol["withdrawal_episodes"],
                             life_id=f"{recipe_name}/{seed}/{arm}/withdrawal", routes=after_routes, seam=seam)
            withdrawn = directory / f"{arm}-withdrawn.npz"
            living.save(withdrawn)
            (directory / f"{arm}-withdrawn.seam.json").write_text(json.dumps(after.seam.to_dict()))
            arm_result["withdrawal"] = {
                "counts": after.counts,
                "summary": episode_summary(after.episodes, make_world(world, route=0).stages),
                "events_sha256": write_jsonl_gz(directory / f"{arm}-withdrawal-events.jsonl.gz", after.events),
                "frozen": frozen(withdrawn),
            }
        arm_result["seconds"] = round(time.time() - started, 2)
        result["arms"][arm] = arm_result
        print(json.dumps({"seed": seed, "recipe": recipe_name, "arm": arm, "seconds": arm_result["seconds"],
                          "sampled": arm_result["frozen"].get("sampled", {}).get("summary", {}).get("success_rate"),
                          "greedy": arm_result["frozen"].get("greedy", {}).get("summary", {}).get("success_rate")}),
              flush=True)
    copier.close()
    rows = []
    for arm, arm_result in result["arms"].items():
        for mode, reading in arm_result.get("frozen", {}).items():
            for row in reading["rows"]:
                rows.append({"recipe": recipe_name, "seed": seed, "arm": arm, "phase": "trained", "mode": mode, **row})
        for mode, reading in arm_result.get("withdrawal", {}).get("frozen", {}).items():
            for row in reading["rows"]:
                rows.append({"recipe": recipe_name, "seed": seed, "arm": arm, "phase": "withdrawn", "mode": mode, **row})
    write_csv(directory / "episodes.csv", rows)
    for arm_result in result["arms"].values():
        for reading in arm_result.get("frozen", {}).values():
            reading.pop("rows", None)
        for reading in arm_result.get("withdrawal", {}).get("frozen", {}).values():
            reading.pop("rows", None)
    (directory / "founder.json").write_text(json.dumps(result, indent=1))
    return result


# -- the whole run


def analytic(world: dict[str, Any]) -> dict[str, Any]:
    probe = make_world(world, route=0)
    exact = uniform_chain_success_exact(probe.actions, probe.stages, probe.deadline)
    if world["kind"] == "cold_chain":
        return {
            "uniform_random_success": float(exact),
            "uniform_random_success_fraction": f"{exact.numerator}/{exact.denominator}",
            "uniform_random_dp": chain_success([1 / probe.actions] * probe.stages, probe.deadline),
        }
    return {"note": "route cue: the context-blind ceiling at the first decision is 0.5"}


def contrasts(results: list[dict[str, Any]], arms: list[str], phase: str = "frozen") -> dict[str, Any]:
    """Founder-paired differences of every trained arm against random and the founder."""
    out: dict[str, Any] = {}
    for mode in ("sampled", "greedy"):
        for arm in arms:
            def rate(result: dict[str, Any], name: str) -> float | None:
                entry = result["arms"].get(name, {})
                if name in CONTROLS:  # controls are read once, at birth
                    frozen = entry.get("frozen", {})
                    reading = frozen.get(mode) or frozen.get("sampled")
                elif phase == "withdrawal":
                    reading = entry.get("withdrawal", {}).get("frozen", {}).get(mode)
                else:
                    reading = entry.get("frozen", {}).get(mode)
                return None if reading is None else reading["summary"]["success_rate"]

            values = [rate(r, arm) for r in results]
            if any(v is None for v in values) or len(values) < 2:
                continue
            for control in ("random", "founder"):
                base = [rate(r, control) for r in results]
                if any(b is None for b in base):
                    continue
                out[f"{mode}:{arm}-{control}"] = paired_bootstrap(values, base)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--protocol", type=Path, default=HERE / "protocol.json")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--seeds", type=int, nargs="*")
    parser.add_argument("--arms", nargs="*")
    parser.add_argument("--recipes", nargs="*")
    parser.add_argument("--wheel-sha256", default=None)
    parser.add_argument("--training-episodes", type=int, default=None,
                        help="development override; marks the run as not the declared protocol")
    parser.add_argument("--evaluation-episodes", type=int, default=None,
                        help="development override; marks the run as not the declared protocol")
    parser.add_argument("--withdrawal-episodes", type=int, default=None,
                        help="development override; marks the run as not the declared protocol")
    args = parser.parse_args(argv)
    protocol, digest = load_protocol(args.protocol)
    overridden = {}
    for name, key in (("training_episodes", args.training_episodes),
                      ("withdrawal_episodes", args.withdrawal_episodes)):
        if key is not None:
            overridden[name] = key
            protocol[name] = key
    if args.evaluation_episodes is not None:
        overridden["evaluation.episodes"] = args.evaluation_episodes
        protocol["evaluation"]["episodes"] = args.evaluation_episodes
    seeds = args.seeds or protocol["seeds"]["development"]
    arms = args.arms or list(protocol["arms"])
    recipes = args.recipes or list(protocol["recipes"])
    if args.out is None:
        parser.error("--out is required")
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "protocol.json").write_bytes(Path(args.protocol).read_bytes())
    manifest = Manifest(protocol_sha256=digest, argv=sys.argv if argv is None else ["runner.py", *argv],
                        wheel_sha256=args.wheel_sha256)
    summary: dict[str, Any] = {"schema": SCHEMA, "protocol_sha256": digest, "overrides": overridden,
                               "declared_protocol": not overridden, "analytic": analytic(protocol["world"]),
                               "recipes": {}}
    for recipe in recipes:
        results = [run_founder(protocol, seed, arms, recipe, args.out) for seed in seeds]
        summary["recipes"][recipe] = {
            "founders": [
                {"seed": r["seed"], "arms": {a: {k: v for k, v in r["arms"][a].items() if k in ("frozen", "withdrawal", "training")}
                                              for a in r["arms"]}}
                for r in results
            ],
            "contrasts": contrasts(results, arms),
            "contrasts_withdrawn": contrasts(results, arms, phase="withdrawal"),
        }
    body = manifest.close({"seeds": seeds, "arms": arms, "recipes": recipes})
    (args.out / "manifest.json").write_text(json.dumps(body, indent=1))
    (args.out / "metrics.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({"out": str(args.out), "wall_seconds": body["wall_seconds"],
                      "peak_rss_bytes": body["peak_rss_bytes"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
