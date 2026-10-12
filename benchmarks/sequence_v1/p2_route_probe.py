"""P2 causal test at the route cue's ambiguous decision.

For each acquired checkpoint two branches of the same frozen brain live through the cue
phase: one sees cue A, the other cue B, with every other input identical. Both then face the
byte-identical first decision. On copies the probe reads the exact next-action distribution:

- ``intact``: each branch as it is;
- ``sham``: a second checkpoint round trip of each branch;
- ``trace_erased``: the branch's working trace reset;
- ``reset``: ``Brain.reset`` on the branch (the broad comparator);
- ``transplant``: the other branch's working trace (``trace``, ``last``, ``cold``) copied in.

The cue phase is lived with greedy ``act`` calls, so the two branches differ only by the cue;
the world ignores those actions. Scores per checkpoint: the probability of the route's
required action and the greedy choice's correctness for intact, sham and erased branches; for
transplants, agreement with the donor's route and with the recipient's own route.

    python p2_route_probe.py --run RUN_DIR --out OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from probes import Copier, read_policy, transplant  # noqa: E402
from worlds import ROUTE_A, ROUTE_B, RouteCue  # noqa: E402


def branch(brain: Any, route: int, neutral: int, copier: Copier) -> tuple[Any, np.ndarray, int]:
    """A copy of ``brain`` that lived the cue phase of ``route``; the first decision's input."""
    copy = copier.copy(brain)
    copy.reset()
    world = RouteCue(route, neutral=neutral)
    while world.cue_phase:
        copy.act(world.observation(), greedy=True)
        world.step(4)  # WAIT; the world ignores actions during the cue phase
    return copy, world.observation(), int(world.required())


def scores(reading: dict[str, Any], required: int) -> dict[str, Any]:
    if not reading.get("qualified", False):
        return {"qualified": False}
    return {
        "qualified": True,
        "p_required": reading["probabilities"][required],
        "greedy_right": int(reading["greedy"] == required),
        "greedy": reading["greedy"],
        "margin": reading["margin"],
        "undecided": reading["undecided"],
    }


def probe_checkpoint(path: Path, neutral: int, copier: Copier) -> dict[str, Any]:
    from cadence import Brain  # noqa: PLC0415

    brain = Brain.load(path)
    a, xa, need_a = branch(brain, ROUTE_A, neutral, copier)
    b, xb, need_b = branch(brain, ROUTE_B, neutral, copier)
    if not np.array_equal(xa, xb):
        raise RuntimeError("the first decision's inputs differ between routes")
    out: dict[str, Any] = {"checkpoint": str(path), "required": {"A": need_a, "B": need_b}}
    for label, own, other, need, other_need in (("A", a, b, need_a, need_b), ("B", b, a, need_b, need_a)):
        intact = read_policy(copier.copy(own), xa)
        sham = read_policy(copier.copy(copier.copy(own)), xa)
        erased_copy = copier.copy(own)
        erased_copy.working_memory.reset(1, rows=np.array([0]))
        erased = read_policy(erased_copy, xa)
        reset_copy = copier.copy(own)
        reset_copy.reset()
        reset = read_policy(reset_copy, xa)
        recipient = copier.copy(own)
        warm = transplant(recipient, other, ("working_memory",))
        moved = read_policy(recipient, xa, warm=warm)
        out[label] = {
            "intact": scores(intact, need),
            "sham": scores(sham, need),
            "trace_erased": scores(erased, need),
            "reset": scores(reset, need),
            "transplant_donor": scores(moved, other_need),
            "transplant_own": scores(moved, need),
        }
    return out


def summarize(cells: list[dict[str, Any]]) -> dict[str, Any]:
    def mean(path: tuple[str, str], field: str) -> float | None:
        values = [c[path[0]][path[1]][field] for c in cells if c[path[0]][path[1]].get("qualified")]
        return float(np.mean(values)) if values else None

    out = {}
    for name in ("intact", "sham", "trace_erased", "reset", "transplant_donor", "transplant_own"):
        out[name] = {
            "p_required": float(np.mean([v for v in (mean((r, name), "p_required") for r in "AB") if v is not None])),
            "greedy_right": float(np.mean([v for v in (mean((r, name), "greedy_right") for r in "AB") if v is not None])),
        }
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--run", type=Path, required=True, help="a runner output directory")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    protocol = json.loads((args.run / "protocol.json").read_text())
    neutral = int(protocol["world"].get("neutral", 2))
    copier = Copier()
    results: dict[str, Any] = {"schema": "route-cue-probe/1", "run": str(args.run), "checkpoints": {}}
    try:
        for founder in sorted(args.run.glob("*/founder-*")):
            for checkpoint in sorted(founder.glob("*-trained.npz")) + [founder / "founder.npz"]:
                arm = checkpoint.name.replace("-trained.npz", "").replace(".npz", "")
                cell = probe_checkpoint(checkpoint, neutral, copier)
                key = f"{founder.name}/{arm}"
                results["checkpoints"][key] = cell
                print(json.dumps({"checkpoint": key,
                                  "intact": [cell[r]["intact"].get("greedy_right") for r in "AB"],
                                  "erased": [cell[r]["trace_erased"].get("greedy_right") for r in "AB"],
                                  "donor": [cell[r]["transplant_donor"].get("greedy_right") for r in "AB"]}),
                      flush=True)
    finally:
        copier.close()
    by_arm: dict[str, list[dict[str, Any]]] = {}
    for key, cell in results["checkpoints"].items():
        by_arm.setdefault(key.split("/")[1], []).append(cell)
    results["by_arm"] = {arm: summarize(cells) for arm, cells in by_arm.items()}
    args.out.write_text(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
