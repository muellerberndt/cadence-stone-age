"""Routine moments and settle steps per moment, from the event logs the runner retained.

    python routine_reading.py RUNS            # ROUTINE_RESULTS.md and routine-summary.json beside the runs

For every run directory ``RUNS/rs-*`` and ``RUNS/rc-*``, recipe, founder, arm and phase (``train``,
``withdrawal``), the events of ``<arm>-<phase>-events.jsonl.gz`` give, per moment:

- ``learning``: the library's learning report for the moment's outcome, recorded when the outcome
  was delivered with the next observation. Through ``Brain.live`` an outcome is learned only when
  the moment that produced it was aroused (its action sampled); a calm moment's outcome is not
  learned and its record is empty. So the share of routine moments through ``live`` is the share
  of moments (the seam's excluded, its outcome being owed) whose record is empty. Through
  ``Brain.step`` every outcome is learned and the share is zero by construction.
- ``choice.settlement.steps``: the solver steps of the settle the moment's action was read from
  (``Brain.last_settlement`` after the call), the measure of a moment's settle here. The arousal
  report's own ``sweeps`` (the routine forecast's settle plus the act's) and ``learning_sweeps``
  are not in the logs; a learned moment's ``learning.free_steps`` (its learning free phase) is.
"""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

PATH_OF = {"step": "step", "live": "live"}


def read(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in gzip.open(path, "rt")]


def measure(events: list[dict[str, Any]], path: str) -> dict[str, Any]:
    outcomes = events[:-1]  # the last event's outcome is owed at the seam
    learned = [e for e in outcomes if isinstance(e.get("learning"), dict) and e["learning"]]
    steps = [e["choice"]["settlement"]["steps"] for e in events
             if isinstance(e.get("choice"), dict) and isinstance(e["choice"].get("settlement"), dict)]
    free = [e["learning"].get("free_steps") for e in learned if e["learning"].get("free_steps") is not None]
    routine = None if path != "live" else (len(outcomes) - len(learned)) / len(outcomes) if outcomes else None
    return {"moments": len(events), "outcomes": len(outcomes), "learned": len(learned),
            "routine_share": routine, "settle_steps_per_moment": float(np.mean(steps)) if steps else None,
            "settle_steps_zero_share": float(np.mean([s == 0 for s in steps])) if steps else None,
            "learning_free_steps_per_learned": float(np.mean(free)) if free else None,
            "refused_attempts": int(sum(int(e["choice"].get("refused_attempts", 0)) for e in events
                                       if isinstance(e.get("choice"), dict)))}


def pooled(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Pool rows by their moment counts."""
    moments = sum(r["moments"] for r in rows)
    outcomes = sum(r["outcomes"] for r in rows)
    learned = sum(r["learned"] for r in rows)
    def weighted(key: str, weight: str) -> float | None:
        pairs = [(r[key], r[weight]) for r in rows if r[key] is not None and r[weight]]
        total = sum(w for _, w in pairs)
        return float(sum(v * w for v, w in pairs) / total) if total else None
    return {"moments": moments, "outcomes": outcomes, "learned": learned,
            "routine_share": (outcomes - learned) / outcomes if outcomes and any(r["routine_share"] is not None for r in rows) else None,
            "settle_steps_per_moment": weighted("settle_steps_per_moment", "moments"),
            "settle_steps_zero_share": weighted("settle_steps_zero_share", "moments"),
            "learning_free_steps_per_learned": weighted("learning_free_steps_per_learned", "learned"),
            "refused_attempts": sum(r["refused_attempts"] for r in rows)}


def fmt(v: Any, digits: int = 3) -> str:
    return "-" if v is None else (f"{v:.{digits}f}" if isinstance(v, float) else str(v))


def main(argv: list[str]) -> int:
    runs = Path(argv[0]).resolve()
    table: dict[str, dict[str, Any]] = {}
    lines = ["# Routine moments and settle steps per moment", "",
             "From the retained event logs (see the module docstring for the definitions). Routine share is "
             "defined through `live` only; through `step` every outcome is learned. Settle steps are the solver "
             "steps of the settle each action was read from; zero means the state already met the tolerance at the "
             "first check. Rows pool the arms of one path and phase over the founders of the run.", ""]
    for run in sorted(list(runs.glob("rs-*")) + list(runs.glob("rc-*"))):
        if not (run / "manifest.json").exists():
            continue
        protocol = json.loads((run / "protocol.json").read_text())
        arms = protocol["arms"]
        per_run: dict[str, Any] = {}
        for recipe_dir in sorted(run.iterdir()):
            if not recipe_dir.is_dir():
                continue
            recipe = recipe_dir.name
            for founder_dir in sorted(recipe_dir.glob("founder-*")):
                seed = int(founder_dir.name.split("-")[1])
                for log in sorted(founder_dir.glob("*-events.jsonl.gz")):
                    arm, phase = log.name[: -len("-events.jsonl.gz")].rsplit("-", 1)
                    path = PATH_OF[arms[arm]["adapter"]] if arm in arms else "?"
                    row = measure(read(log), path)
                    row.update(recipe=recipe, seed=seed, arm=arm, phase=phase, path=path)
                    per_run.setdefault(recipe, []).append(row)
        table[run.name] = per_run
        lines += [f"## {run.name}", "",
                  "| recipe | path | phase | founders | arms | moments | outcomes | learned | routine share | settle steps per moment | settles at zero steps | learning free steps per learned moment | refused |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for recipe, rows in per_run.items():
            for path in ("step", "live"):
                for phase in ("train", "withdrawal"):
                    chosen = [r for r in rows if r["path"] == path and r["phase"] == phase]
                    if not chosen:
                        continue
                    p = pooled(chosen)
                    founders = sorted({r["seed"] for r in chosen})
                    names = sorted({r["arm"] for r in chosen})
                    lines.append(f"| {recipe} | {path} | {phase} | {len(founders)} | {len(names)} | {p['moments']} | {p['outcomes']} | {p['learned']} | "
                                 f"{fmt(p['routine_share'])} | {fmt(p['settle_steps_per_moment'], 1)} | {fmt(p['settle_steps_zero_share'])} | "
                                 f"{fmt(p['learning_free_steps_per_learned'], 1)} | {p['refused_attempts']} |")
        lines.append("")
        # per arm for the live path, where the routine share is defined
        live_rows = [r for rows in per_run.values() for r in rows if r["path"] == "live"]
        if live_rows:
            lines += ["Per arm through `live`:", "",
                      "| recipe | founder | arm | phase | outcomes | learned | routine share | settle steps per moment | learning free steps per learned moment |",
                      "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
            for r in sorted(live_rows, key=lambda r: (r["arm"], r["phase"], r["recipe"], r["seed"])):
                lines.append(f"| {r['recipe']} | {r['seed']} | {r['arm']} | {r['phase']} | {r['outcomes']} | {r['learned']} | "
                             f"{fmt(r['routine_share'])} | {fmt(r['settle_steps_per_moment'], 1)} | {fmt(r['learning_free_steps_per_learned'], 1)} |")
            lines.append("")
    (runs / "ROUTINE_RESULTS.md").write_text("\n".join(lines) + "\n")
    (runs / "routine-summary.json").write_text(json.dumps(table, indent=1))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
