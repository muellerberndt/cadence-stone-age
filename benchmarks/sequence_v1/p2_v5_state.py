"""P2, first step: which runtime state does an acquired V5 brain use within an episode?

Frozen copies of acquired checkpoints run V5's sampled evaluation (reset at each episode
start, ``act`` at every decision). Before each decision the exact next-action distribution is
read on copies under every intervention of ``probes.py``; the living copy then acts with its
own stream. Readings are stratified by stage and decisions elapsed.

Two summaries per checkpoint:

- the mean probability of the required action and the total-variation distance to the intact
  distribution, per intervention and stage;
- a memoryless chain: the success the dynamic programme predicts from the reset readings
  (V5's fingerprint, read exactly), against the observed sequential success. A gap says the
  episode's own state changes the policy; which state carries it is read from the selective
  interventions.

    python p2_v5_state.py --checkpoints DIR --out OUT.json --episodes 50
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from adapters import readout  # noqa: E402
from metrics import chain_success  # noqa: E402
from probes import INTERVENTIONS, Copier, probe, reseed_actions, state_digest  # noqa: E402
from runner import stream_seed  # noqa: E402
from worlds import ColdChain, action_id  # noqa: E402

ARMS = ("founder", "natural_only", "grade_only", "corrective_teacher")


def checkpoint_path(directory: Path, arm: str, seed: int) -> Path:
    if arm == "founder":
        return directory / f"historical_reproduction_founder_seed_{seed}.npz"
    return directory / f"historical_reproduction_{arm}_trained_seed_{seed}.npz"


def tv(p: list[float], q: list[float]) -> float:
    return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())


def run_checkpoint(path: Path, seed: int, arm: str, episodes: int, copier: Copier) -> dict[str, Any]:
    from cadence import Brain  # noqa: PLC0415

    brain = Brain.load(path)
    digest = state_digest(brain, copier)
    reseed_actions(brain, stream_seed(11, seed, ARMS.index(arm)))
    points = []
    outcomes = []
    for episode in range(episodes):
        brain.reset()
        world = ColdChain()
        history: list[int] = []
        while not world.done:
            x = world.observation()
            readings = probe(brain, x, INTERVENTIONS, copier)
            required = world.required()
            point = {
                "episode": episode,
                "decision": world.decisions,
                "stage": world.stage,
                "history": list(history),
                "required": required,
            }
            for name, reading in readings.items():
                if not reading.get("applicable", True) or not reading.get("qualified", False):
                    point[name] = None
                    continue
                point[name] = {
                    "p": reading["probabilities"],
                    "greedy": reading["greedy"],
                    "margin": reading["margin"],
                    "undecided": reading["undecided"],
                }
            out = brain.act(x, greedy=False)
            action = action_id(out, world.actions)
            acted = readout(brain)
            # the probe's intact reading must be the policy the brain then sampled from
            point["intact_matches_act"] = bool(
                point["intact"] is not None
                and np.allclose(point["intact"]["p"], acted["probabilities"], atol=1e-9)
            )
            point["action"] = action
            points.append(point)
            history.append(action)
            world.step(action)
        outcomes.append({"episode": episode, "success": world.success, "decisions": world.decisions})
    if state_digest(Brain.load(path), copier) != digest:
        raise RuntimeError("the checkpoint changed on disk during probing")
    return {"seed": seed, "arm": arm, "checkpoint_digest": digest, "points": points, "outcomes": outcomes}


def summarize(run: dict[str, Any]) -> dict[str, Any]:
    by: dict[tuple[str, int], list[float]] = defaultdict(list)
    tvs: dict[tuple[str, int], list[float]] = defaultdict(list)
    greedy_change: dict[tuple[str, int], list[int]] = defaultdict(list)
    reset_advance: dict[int, list[float]] = defaultdict(list)
    for point in run["points"]:
        stage, required = point["stage"], point["required"]
        intact = point["intact"]
        for name in INTERVENTIONS:
            reading = point.get(name)
            if reading is None or intact is None:
                continue
            by[(name, stage)].append(reading["p"][required])
            tvs[(name, stage)].append(tv(reading["p"], intact["p"]))
            greedy_change[(name, stage)].append(int(reading["greedy"] != intact["greedy"]))
        if point.get("full_reset") is not None:
            reset_advance[stage].append(point["full_reset"]["p"][required])
    # V5's fingerprint, exactly: a reset brain's probability of the required action per stage
    fingerprint = [float(np.mean(reset_advance[s])) if reset_advance[s] else 0.0 for s in range(4)]
    observed = float(np.mean([o["success"] for o in run["outcomes"]]))
    table = {}
    for (name, stage), values in sorted(by.items()):
        table.setdefault(name, {})[str(stage)] = {
            "p_required": float(np.mean(values)),
            "tv_to_intact": float(np.mean(tvs[(name, stage)])),
            "greedy_changed": float(np.mean(greedy_change[(name, stage)])),
            "points": len(values),
        }
    return {
        "seed": run["seed"],
        "arm": run["arm"],
        "observed_success": observed,
        "memoryless_from_reset": chain_success(fingerprint, 10),
        "reset_fingerprint": fingerprint,
        "intact_matches_act": float(np.mean([p["intact_matches_act"] for p in run["points"]])),
        "undecided_intact": float(np.mean([bool(p["intact"] and p["intact"]["undecided"]) for p in run["points"]])),
        "by_intervention": table,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--checkpoints", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--episodes", type=int, default=50)
    parser.add_argument("--seeds", type=int, nargs="*", default=[42, 43, 44, 45, 46])
    parser.add_argument("--arms", nargs="*", default=list(ARMS))
    args = parser.parse_args(argv)
    started = time.time()
    copier = Copier()
    runs, summaries = [], []
    try:
        for seed in args.seeds:
            for arm in args.arms:
                run = run_checkpoint(checkpoint_path(args.checkpoints, arm, seed), seed, arm, args.episodes, copier)
                summary = summarize(run)
                runs.append(run)
                summaries.append(summary)
                print(json.dumps({k: summary[k] for k in ("seed", "arm", "observed_success", "memoryless_from_reset", "intact_matches_act")}), flush=True)
    finally:
        copier.close()
    args.out.write_text(json.dumps({"schema": "v5-state-probe/1", "episodes": args.episodes,
                                    "seconds": round(time.time() - started, 1),
                                    "summaries": summaries, "runs": runs}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
