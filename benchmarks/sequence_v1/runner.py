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
import copy
import csv
import functools
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
    never_repeat_chain_success_exact,
    paired_bootstrap,
    uniform_chain_success_exact,
)
from probes import Copier, reseed_actions, state_digest  # noqa: E402
from receipts import Manifest, canonical  # noqa: E402
from worlds import (  # noqa: E402
    WEATHER_SEEN,
    WEATHER_UNSEEN,
    action_id,
    balanced_routes,
    chain_situations,
    make_world,
    recall_schedule,
    weather_cell,
    weather_cycle,
    weather_schedule,
)

SCHEMA = "stone-age-sequence/1"
CONTROLS = ("founder", "random", "oracle", "searcher")
STREAM = {"evaluation": 1, "random": 2, "routes": 3, "withdrawal_routes": 4, "searcher": 5,
          "labels": 6, "per_state": 7}
CHAIN_WORLDS = ("cold_chain", "weather_chain")
CAREGIVERS = ("none", "grade", "correct", "guide", "random_label")
TEACHING_KEYS = ("adapter", "caregiver", "compose", "training_episodes")


def load_protocol(path: Path) -> tuple[dict[str, Any], str]:
    raw = Path(path).read_bytes()
    protocol = json.loads(raw)
    if protocol.get("schema") != SCHEMA:
        raise ValueError(f"protocol schema must be {SCHEMA}")
    seen: list[str] = []
    for name, arm in protocol["arms"].items():
        if arm["adapter"] not in ADAPTERS:
            raise ValueError(f"arm {name}: unknown adapter {arm['adapter']!r}")
        if arm["caregiver"] not in CAREGIVERS:
            raise ValueError(f"arm {name}: unknown caregiver {arm['caregiver']!r}")
        if arm["adapter"] == "live" and arm["caregiver"] in ("correct", "guide", "random_label"):
            raise ValueError(f"arm {name}: live takes no teacher; declare an ordering first")
        if arm.get("withdrawal_adapter", arm["adapter"]) not in ADAPTERS:
            raise ValueError(f"arm {name}: unknown withdrawal adapter {arm['withdrawal_adapter']!r}")
        if "training_episodes" in arm and int(arm["training_episodes"]) < 1:
            raise ValueError(f"arm {name}: an arm's own training runs at least one episode")
        twin = arm.get("twin_of")
        if twin is not None:
            if twin not in seen:
                raise ValueError(f"arm {name}: its twin {twin!r} must be an earlier arm")
            source = protocol["arms"][twin]
            if any(arm.get(k) != source.get(k) for k in TEACHING_KEYS):
                raise ValueError(f"arm {name}: a twin is taught exactly as {twin!r}")
        seen.append(name)
    marks = protocol.get("withdrawal_checkpoints", [])
    if marks and not all(0 < int(k) < protocol.get("withdrawal_episodes", 0) for k in marks):
        raise ValueError("withdrawal checkpoints lie strictly inside the withdrawal life")
    if marks != sorted(set(marks)):
        raise ValueError("withdrawal checkpoints are distinct and increasing")
    if int(protocol["evaluation"].get("per_state_samples", 0)) < 0:
        raise ValueError("per-state samples are a nonnegative count")
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
    # The motor readout's bias at birth (zero in every released composition), set once after
    # composing; it stays plastic.
    motor_bias = float(options.pop("motor_bias", 0.0))
    probe = make_world(world, route=0)
    brain = Brain.compose(inputs=probe.inputs, actions=probe.actions, seed=int(seed), **options)
    if motor_bias:
        graph = brain.brain
        bias = graph.bias.copy()
        bias[np.asarray(brain.motor_index)] = motor_bias
        brain.learner.brain = graph.with_parameters(bias=bias)
    return brain


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
    the brain's input.

    ``random_label`` is the null teacher of Will Glynn's cadence-teachers, EXP-52 and EXP-53
    (https://github.com/WGlynn/cadence-teachers, experiments/EXP-53.md): it speaks at exactly
    the moments ``correct`` does, but its label is a uniformly random action of the alphabet
    from its own stream (``rng``). Its twin taught by ``correct`` measures what the content of
    a label adds to the fact of being corrected."""

    kind: str
    guided_span: int
    autonomous_span: int
    right: float = 0.5
    wrong: float = -0.5
    rng: np.random.Generator | None = None

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
        if self.kind not in ("correct", "random_label") or not guided or not outcome.decision:
            return None
        if outcome.advanced or outcome.done:
            return None
        if self.kind == "random_label":
            if self.rng is None:
                raise ValueError("the random-label caregiver needs its own random stream")
            return int(self.rng.integers(world.actions))
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


def run_withdrawal(
    adapter: Any,
    world_spec: dict[str, Any],
    episodes: int,
    *,
    life_id: str,
    seam: PendingOutcome,
    routes: list[Any] | None = None,
    marks: list[int] | tuple[int, ...] = (),
    at_mark: Any = None,
) -> Life:
    """The caregiver-free life of ``episodes`` episodes, resumed from ``seam``. At every mark the
    life stops at a seam, ``at_mark(mark, seam)`` saves and reads a copy, and the same adapter
    resumes the life from that seam, so the stops leave it exactly as it would have run
    (``tests/test_contracts.py`` checks this). Reading a taught brain over time while it lives
    alone is Will Glynn's design in cadence-teachers, EXP-47
    (https://github.com/WGlynn/cadence-teachers, experiments/EXP-47.md)."""
    parts: list[tuple[int, Life]] = []
    start = 0
    for mark in [*marks, episodes]:
        part = run_life(adapter, world_spec, Caregiver("none", 0, 1), mark - start,
                        life_id=life_id, routes=None if routes is None else routes[start:mark],
                        seam=seam)
        parts.append((start, part))
        seam = part.seam
        if mark < episodes and at_mark is not None:
            at_mark(mark, seam)
        start = mark
    if len(parts) == 1:
        return parts[0][1]
    events: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    decisions = 0
    teaching: dict[str, int] = {}
    for offset, part in parts:
        if events:
            # the stop's held outcome was learned when the life resumed: record it on its event,
            # as the uninterrupted life does
            events[-1].pop("held", None)
            events[-1]["learning"] = part.counts["resumed_learning"]
        for event in part.events:
            event = dict(event, episode=event["episode"] + offset)
            if event["decision"] is not None:
                event["decision"] += decisions
            events.append(event)
        summaries += [dict(s, episode=s["episode"] + offset) for s in part.episodes]
        decisions += part.counts["decisions"]
        for key, value in part.counts["teaching"].items():
            teaching[key] = teaching.get(key, 0) + value
    last = parts[-1][1]
    counts = dict(last.counts)  # refusals and the ledger are the shared adapter's, whole-life
    counts.update(resumed_learning=parts[0][1].counts["resumed_learning"], decisions=decisions,
                  events=len(events), episodes=len(summaries), teaching=teaching,
                  checkpoints=[offset for offset, _ in parts[1:]])
    return Life(events, last.seam, summaries, counts)


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
    """Uniform random over the alphabet, the stage-aware oracle that reads the scorer (a
    scorer sanity check, never a Cadence answer path), or, on a chain world, the never-repeat
    searcher of Will Glynn's cadence-teachers, EXP-45: it knows nothing of the chain, sees only
    the observation, and never repeats an action after which the observation stayed the same
    within the episode. On V5's chain it succeeds with probability exactly .304, the chance
    level a free-retry chamber sets for a brain that searches instead of knowing."""
    if kind == "searcher" and world_spec["kind"] not in CHAIN_WORLDS:
        raise ValueError("the never-repeat searcher is defined on chain worlds")
    rng = np.random.default_rng(seed)
    rows = []
    for index in range(episodes):
        world = make_world(world_spec, None if routes is None else routes[index])
        failed: dict[str, set[int]] = {}
        while not world.done:
            if kind == "random":
                action = int(rng.integers(world.actions))
            elif kind == "searcher":
                x = world.observation()
                tried = failed.setdefault(observation_digest(x), set())
                options = [a for a in range(world.actions) if a not in tried] or list(range(world.actions))
                action = int(options[int(rng.integers(len(options)))])
            else:
                required = world.required()
                # no decision is due: any valid action, the world ignores it
                action = 0 if required is None else int(required)
            world.step(action)
            if kind == "searcher" and not world.done and np.array_equal(world.observation(), x):
                tried.add(action)
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


# -- per-state reading
#
# Will Glynn's reading in cadence-teachers, EXP-45, EXP-46 and EXP-48
# (https://github.com/WGlynn/cadence-teachers): every stage of the chain is read on its own, from
# a reset copy, greedily. A brain that searches inside an attempt cannot pass it, so it says
# whether the chain was learned where whole-chain success can be search. On the weather chain
# every stage is read under each taught and each unseen weather.


def situation_sets(world_spec: dict[str, Any]) -> dict[str, list[Any]]:
    """The cells of a per-state reading: the chain itself, or every declared weather."""
    if world_spec["kind"] == "weather_chain":
        return {
            name: [{"weather": list(weather_cell(w))} for w in world_spec.get(name, default)]
            for name, default in (("seen", WEATHER_SEEN), ("unseen", WEATHER_UNSEEN))
        }
    return {"chain": [None]}


def per_state(checkpoint: Path, world_spec: dict[str, Any], *, samples: int = 0,
              seed: int = 0) -> dict[str, Any]:
    """Per-state greedy accuracy of a frozen copy: for every situation, ``Brain.reset`` and one
    greedy ``act``. With ``samples``, also each stage's sampled probability of the required
    action (``samples`` reset draws, EXP-45's 300) and the success a memoryless policy with those
    probabilities would have, to set beside the sampled whole-chain success."""
    from cadence import Brain  # noqa: PLC0415

    brain = Brain.load(checkpoint)
    reseed_actions(brain, seed)
    probe = make_world(world_spec, None)
    deadline, actions = probe.deadline, probe.actions
    out: dict[str, Any] = {}
    for name, cells in situation_sets(world_spec).items():
        rows: list[dict[str, Any]] = []
        memoryless = []
        for cell in cells:
            stage_p = []
            for stage, x, required in chain_situations(world_spec, cell):
                row: dict[str, Any] = {"stage": stage, "required": required,
                                       "weather": None if cell is None else cell["weather"]}
                try:
                    brain.reset()
                    row["greedy"] = action_id(brain.act(x, greedy=True), actions)
                    row["right"] = row["greedy"] == required
                except RuntimeError:
                    row.update(greedy=None, right=False, refused=True)
                if samples:
                    hits = 0
                    for _ in range(samples):
                        brain.reset()
                        hits += int(action_id(brain.act(x, greedy=False), actions) == required)
                    row["p_right"] = hits / samples
                    stage_p.append(row["p_right"])
                rows.append(row)
            if samples:
                memoryless.append(chain_success(stage_p, deadline))
        stages = sorted({r["stage"] for r in rows})
        reading: dict[str, Any] = {
            "situations": len(rows),
            "accuracy": float(np.mean([r["right"] for r in rows])),
            "all_right": all(r["right"] for r in rows),
            "stage_accuracy": [float(np.mean([r["right"] for r in rows if r["stage"] == s]))
                               for s in stages],
            "refused": sum(1 for r in rows if r.get("refused")),
            "rows": rows,
        }
        if samples:
            reading["samples"] = samples
            reading["stage_p_right"] = [float(np.mean([r["p_right"] for r in rows if r["stage"] == s]))
                                        for s in stages]
            reading["memoryless_success"] = float(np.mean(memoryless))
        out[name] = reading
    if "seen" in out and "unseen" in out:
        out["gap"] = out["seen"]["accuracy"] - out["unseen"]["accuracy"]
    return out


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


def schedules(protocol: dict[str, Any], seed: int, training: int) -> tuple[Any, Any, Any]:
    """Each life's episode cells for one founder, shared by every arm: route cue routes,
    recall cells or weathers for training (``training`` episodes, the longest arm's), for the
    withdrawal life and for the frozen evaluations; ``None`` for the plain chain. A longer
    schedule begins with the shorter one, so an arm's own lesson length never moves another's."""
    world, evaluation = protocol["world"], protocol["evaluation"]
    kind = world["kind"]
    withdrawal = protocol.get("withdrawal_episodes", 0)

    def rng(*parts: int) -> np.random.Generator:
        return np.random.default_rng(stream_seed(*parts))

    if kind == "weather_chain":
        seen = tuple(weather_cell(w) for w in world.get("seen", WEATHER_SEEN))
        unseen = tuple(weather_cell(w) for w in world.get("unseen", WEATHER_UNSEEN))
        return (
            weather_schedule(training, rng(STREAM["routes"], seed), seen),
            weather_schedule(withdrawal, rng(STREAM["withdrawal_routes"], seed), seen) if withdrawal > 0 else None,
            weather_cycle(evaluation["episodes"], unseen),
        )
    if kind not in ("route_cue", "recall"):
        return None, None, None
    schedule_of = recall_schedule if kind == "recall" else balanced_routes
    return (
        schedule_of(training, rng(STREAM["routes"], seed)),
        schedule_of(withdrawal, rng(STREAM["withdrawal_routes"], seed)) if withdrawal > 0 else None,
        schedule_of(evaluation["episodes"], rng(STREAM["routes"], seed, 1)),
    )


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
    kind = world["kind"]
    lengths = {a: int(protocol["arms"][a].get("training_episodes", protocol["training_episodes"])) for a in arms}
    train_routes, after_routes, eval_routes = schedules(
        protocol, seed, max(lengths.values(), default=protocol["training_episodes"]))

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

    def states(checkpoint: Path) -> dict[str, Any] | None:
        if kind not in CHAIN_WORLDS:
            return None
        return per_state(checkpoint, world, samples=int(evaluation.get("per_state_samples", 0)),
                         seed=stream_seed(STREAM["per_state"], seed))

    result["arms"]["founder"] = {"frozen": frozen(founder_path)}
    if kind in CHAIN_WORLDS:
        result["arms"]["founder"]["per_state"] = states(founder_path)
    for control in ("random", "oracle", "searcher") if kind in CHAIN_WORLDS else ("random", "oracle"):
        stream = STREAM["searcher"] if control == "searcher" else STREAM["random"]
        rows = control_rows(control, world, episodes=evaluation["episodes"],
                            seed=stream_seed(stream, seed), routes=eval_routes)
        result["arms"][control] = {"frozen": {"sampled": {"summary": episode_summary(rows, make_world(world, route=0).stages), "rows": rows}}}

    def read_checkpoint(arm: str, living: Any, store: dict[str, Any], mark: int,
                        held: PendingOutcome) -> None:
        """A copy of the living brain at a withdrawal checkpoint, saved with its seam and read."""
        path = directory / f"{arm}-withdrawal-{mark}.npz"
        living.save(path)
        (directory / f"{arm}-withdrawal-{mark}.seam.json").write_text(json.dumps(held.to_dict()))
        reading: dict[str, Any] = {"frozen": frozen(path)}
        if kind in CHAIN_WORLDS:
            reading["per_state"] = states(path)
        store[str(mark)] = reading

    taught: dict[str, dict[str, Any]] = {}
    for arm in arms:
        spec = protocol["arms"][arm]
        started = time.time()
        twin = spec.get("twin_of")
        if twin in taught:
            # Will Glynn's pairing in cadence-teachers, EXP-47: this arm continues from the very
            # brain and seam its twin was taught into, so the two continuations differ only in
            # what follows the caregiver's leaving.
            trained, seam_path = taught[twin]["checkpoint"], taught[twin]["seam"]
            arm_result: dict[str, Any] = {"spec": spec, "taught_with": twin}
            arm_result.update(copy.deepcopy({k: v for k, v in taught[twin]["result"].items()
                                             if k in ("training", "trained_digest", "events_sha256", "frozen", "per_state")}))
        else:
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
            labels = (np.random.default_rng(stream_seed(STREAM["labels"], seed))
                      if spec["caregiver"] == "random_label" else None)
            caregiver = Caregiver(spec["caregiver"], schedule["guided"], schedule["autonomous"], rng=labels)
            life = run_life(adapter, world, caregiver, lengths[arm],
                            life_id=f"{recipe_name}/{seed}/{arm}/train", routes=train_routes)
            trained = directory / f"{arm}-trained.npz"
            brain.save(trained)
            seam_path = directory / f"{arm}-trained.seam.json"
            seam_path.write_text(json.dumps(life.seam.to_dict()))
            arm_result = {
                "spec": spec,
                "training": {"counts": life.counts, "summary": episode_summary(life.episodes, make_world(world, route=0).stages)},
                "trained_digest": state_digest(brain, copier),
                "events_sha256": write_jsonl_gz(directory / f"{arm}-train-events.jsonl.gz", life.events),
                "frozen": frozen(trained),
            }
            if kind in CHAIN_WORLDS:
                arm_result["per_state"] = states(trained)
            taught[arm] = {"checkpoint": trained, "seam": seam_path, "result": arm_result}
        if protocol.get("withdrawal_episodes", 0) > 0:
            living = Brain.load(trained)
            seam = PendingOutcome(**json.loads(seam_path.read_text()))
            # the life after the caregiver leaves may go on through another interface
            follow = ADAPTERS[spec.get("withdrawal_adapter", spec["adapter"])](living, make_world(world, route=0).actions)
            checkpoints: dict[str, Any] = {}
            after = run_withdrawal(follow, world, protocol["withdrawal_episodes"],
                                   life_id=f"{recipe_name}/{seed}/{arm}/withdrawal", seam=seam,
                                   routes=after_routes,
                                   marks=[int(k) for k in protocol.get("withdrawal_checkpoints", [])],
                                   at_mark=functools.partial(read_checkpoint, arm, living, checkpoints))
            withdrawn = directory / f"{arm}-withdrawn.npz"
            living.save(withdrawn)
            (directory / f"{arm}-withdrawn.seam.json").write_text(json.dumps(after.seam.to_dict()))
            arm_result["withdrawal"] = {
                "counts": after.counts,
                "summary": episode_summary(after.episodes, make_world(world, route=0).stages),
                "events_sha256": write_jsonl_gz(directory / f"{arm}-withdrawal-events.jsonl.gz", after.events),
                "frozen": frozen(withdrawn),
            }
            if kind in CHAIN_WORLDS:
                arm_result["withdrawal"]["per_state"] = states(withdrawn)
            if checkpoints:
                arm_result["withdrawal"]["checkpoints"] = checkpoints
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
        for mark, checkpoint in arm_result.get("withdrawal", {}).get("checkpoints", {}).items():
            for mode, reading in checkpoint["frozen"].items():
                for row in reading["rows"]:
                    rows.append({"recipe": recipe_name, "seed": seed, "arm": arm, "phase": f"withdrawal-{mark}",
                                 "mode": mode, **row})
        for mode, reading in arm_result.get("withdrawal", {}).get("frozen", {}).items():
            for row in reading["rows"]:
                rows.append({"recipe": recipe_name, "seed": seed, "arm": arm, "phase": "withdrawn", "mode": mode, **row})
    write_csv(directory / "episodes.csv", rows)
    for arm_result in result["arms"].values():
        for reading in arm_result.get("frozen", {}).values():
            reading.pop("rows", None)
        for reading in arm_result.get("withdrawal", {}).get("frozen", {}).values():
            reading.pop("rows", None)
        for checkpoint in arm_result.get("withdrawal", {}).get("checkpoints", {}).values():
            for reading in checkpoint["frozen"].values():
                reading.pop("rows", None)
    (directory / "founder.json").write_text(json.dumps(result, indent=1))
    return result


# -- the whole run


def analytic(world: dict[str, Any]) -> dict[str, Any]:
    probe = make_world(world, route=0)
    exact = uniform_chain_success_exact(probe.actions, probe.stages, probe.deadline)
    if world["kind"] in CHAIN_WORLDS:
        searcher = never_repeat_chain_success_exact(probe.actions, probe.stages, probe.deadline)
        return {
            "uniform_random_success": float(exact),
            "uniform_random_success_fraction": f"{exact.numerator}/{exact.denominator}",
            "uniform_random_dp": chain_success([1 / probe.actions] * probe.stages, probe.deadline),
            "never_repeat_searcher_success": float(searcher),
            "never_repeat_searcher_success_fraction": f"{searcher.numerator}/{searcher.denominator}",
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
            for control in ("random", "founder", "searcher"):
                base = [rate(r, control) for r in results]
                if any(b is None for b in base):
                    continue
                out[f"{mode}:{arm}-{control}"] = paired_bootstrap(values, base)
    return out


def phases(protocol: dict[str, Any]) -> list[str]:
    """The readings of an arm in order: after teaching, at each withdrawal checkpoint, at the end."""
    out = ["trained"] + [str(k) for k in protocol.get("withdrawal_checkpoints", [])]
    return out + (["withdrawn"] if protocol.get("withdrawal_episodes", 0) > 0 else [])


def reading_of(result: dict[str, Any], arm: str, phase: str) -> dict[str, Any]:
    """An arm's frozen and per-state readings at one phase; empty when it has none."""
    entry = result["arms"].get(arm, {})
    if phase == "trained":
        return {"frozen": entry.get("frozen", {}), "per_state": entry.get("per_state")}
    withdrawal = entry.get("withdrawal", {})
    if phase == "withdrawn":
        return {"frozen": withdrawal.get("frozen", {}), "per_state": withdrawal.get("per_state")}
    return withdrawal.get("checkpoints", {}).get(phase, {})


def per_state_summary(results: list[dict[str, Any]], arms: list[str], protocol: dict[str, Any]) -> dict[str, Any]:
    """Founder means of the per-state readings, the founders with every situation right, and
    the seen-minus-unseen gap of the weather chain, founder-paired (EXP-48's generalization gap)."""
    out: dict[str, Any] = {}
    for arm in ["founder", *arms]:
        for phase in phases(protocol) if arm != "founder" else ["trained"]:
            readings = [reading_of(r, arm, phase).get("per_state") for r in results]
            if not readings or any(x is None for x in readings):
                continue
            entry: dict[str, Any] = {}
            for name in (n for n in readings[0] if n != "gap"):
                accuracy = [x[name]["accuracy"] for x in readings]
                entry[name] = {"accuracy": float(np.mean(accuracy)), "per_founder": accuracy,
                               "all_right": sum(bool(x[name]["all_right"]) for x in readings),
                               "founders": len(readings)}
                if "memoryless_success" in readings[0][name]:
                    entry[name]["memoryless_success"] = float(np.mean([x[name]["memoryless_success"] for x in readings]))
            if "gap" in readings[0]:
                entry["gap"] = paired_bootstrap([x["seen"]["accuracy"] for x in readings],
                                                [x["unseen"]["accuracy"] for x in readings])
            out[f"{arm}:{phase}"] = entry
    return out


def pair_contrasts(results: list[dict[str, Any]], protocol: dict[str, Any]) -> dict[str, Any]:
    """Founder-paired differences of the arm pairs a protocol declares under
    ``analysis.pairs``, at every phase: per-state accuracy of every situation set and frozen
    success. EXP-53's content measure is such a pair: a lesson's correcting arm minus its
    random-label twin."""
    out: dict[str, Any] = {}
    for candidate, control in protocol.get("analysis", {}).get("pairs", []):
        for phase in phases(protocol):
            a = [reading_of(r, candidate, phase) for r in results]
            b = [reading_of(r, control, phase) for r in results]
            if not a or any(not x for x in a + b):
                continue
            if all(x.get("per_state") for x in a + b):
                for name in (n for n in a[0]["per_state"] if n != "gap"):
                    out[f"per_state:{name}:{phase}:{candidate}-{control}"] = paired_bootstrap(
                        [x["per_state"][name]["accuracy"] for x in a], [x["per_state"][name]["accuracy"] for x in b])
            for mode in ("sampled", "greedy"):
                va = [x["frozen"].get(mode, {}).get("summary", {}).get("success_rate") for x in a]
                vb = [x["frozen"].get(mode, {}).get("summary", {}).get("success_rate") for x in b]
                if any(v is None for v in va + vb):
                    continue
                out[f"{mode}:{phase}:{candidate}-{control}"] = paired_bootstrap(va, vb)
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
    if args.training_episodes is not None:
        for spec in protocol["arms"].values():  # an arm's own lesson length is overridden too
            if "training_episodes" in spec:
                spec["training_episodes"] = args.training_episodes
    if args.withdrawal_episodes is not None and protocol.get("withdrawal_checkpoints"):
        marks = [k for k in protocol["withdrawal_checkpoints"] if k < args.withdrawal_episodes]
        overridden["withdrawal_checkpoints"] = marks
        protocol["withdrawal_checkpoints"] = marks
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
                {"seed": r["seed"], "arms": {a: {k: v for k, v in r["arms"][a].items()
                                                 if k in ("frozen", "withdrawal", "training", "per_state", "taught_with")}
                                              for a in r["arms"]}}
                for r in results
            ],
            "contrasts": contrasts(results, arms),
            "contrasts_withdrawn": contrasts(results, arms, phase="withdrawal"),
            "per_state": per_state_summary(results, arms, protocol),
            "pairs": pair_contrasts(results, protocol),
        }
    body = manifest.close({"seeds": seeds, "arms": arms, "recipes": recipes})
    (args.out / "manifest.json").write_text(json.dumps(body, indent=1))
    (args.out / "metrics.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({"out": str(args.out), "wall_seconds": body["wall_seconds"],
                      "peak_rss_bytes": body["peak_rss_bytes"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
