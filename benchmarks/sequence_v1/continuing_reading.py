"""The recall memory kept across episodes and keyed by its predecessor
(``protocol-continuing-screen.json``, ``protocol-continuing-p1.json``): read the runs.

    python continuing_reading.py RUNS   # CONTINUING_RESULTS.md and continuing-summary.json in RUNS

``RUNS`` holds ``screen-<view>/s<seed>/<recipe>/founder-<seed>/founder.json`` and
``p1/s<seed>/<recipe>/founder-<seed>/founder.json``. C1 is ``keep_pred - base`` per view, C2 the two
options alone, C3 preservation (``keep_pred - founder`` at or above -.05 on every view) and the P1
gate on ``keep_pred - founder``; intervals resample founders (``metrics.paired_bootstrap``), each
founder's arms averaged on the screen.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

import recall_screen as rs
from metrics import paired_bootstrap

VIEWS = ("hidden", "invisible", "visible", "consecutive")
RECIPES = ("founder", "recall", "base", "keep", "pred", "keep_pred")
PAIRS = (("keep_pred", "base"), ("keep", "base"), ("pred", "base"), ("keep_pred", "founder"),
         ("base", "recall"), ("recall", "founder"))
P1_ARMS = ("natural_step", "grade_step", "correct_step", "correct_step_qualified", "natural_live",
           "grade_live")
MARGIN = -0.05
P1_READINGS = (("sampled after teaching", lambda a: rs.sampled(a)),
               ("sampled after the episodes alone", lambda a: rs.sampled(a, "withdrawn")))


def bodies(runs: Path, reading: str) -> dict[str, dict[int, dict[str, Any]]]:
    out: dict[str, dict[int, dict[str, Any]]] = {recipe: {} for recipe in RECIPES}
    for part in sorted((runs / reading).glob("s*")):
        for recipe in RECIPES:
            out[recipe].update(rs.founder_files(part, recipe))
    return out


def cell(c: dict[str, Any]) -> str:
    low, high = c["bootstrap_95"]
    signs = f"{c['positive']}/{c['negative']}/{c['zero']}"
    return f"{c['mean_difference']:+.3f} [{low:+.3f}, {high:+.3f}] ({signs})"


def head(first: str) -> list[str]:
    names = [f"{a} - {b}" for a, b in PAIRS]
    return [f"| {first} | " + " | ".join(RECIPES) + " | " + " | ".join(names) + " |",
            "| --- |" + " --- |" * (len(RECIPES) + len(PAIRS))]


def screen(runs: Path) -> tuple[list[str], dict[str, Any]]:
    lines = ["## The screen (sampled success; recipe means, then paired differences)", ""]
    lines += head("View")
    out: dict[str, Any] = {}
    for view in VIEWS:
        found = bodies(runs, f"screen-{view}")
        seeds = sorted(set.intersection(*(set(found[r]) for r in RECIPES)))
        if not seeds:
            continue
        table = {r: np.array([[rs.sampled(found[r][s]["arms"][arm]) for arm in rs.ARMS] for s in seeds],
                             dtype=float) for r in RECIPES}
        per = {r: table[r].mean(axis=1) for r in RECIPES}
        contrasts = {f"{a} - {b}": paired_bootstrap(per[a], per[b]) for a, b in PAIRS}
        c3 = float((table["keep_pred"] - table["founder"]).mean())
        out[view] = {"founders": seeds, "means": {r: float(table[r].mean()) for r in RECIPES},
                     "contrasts": contrasts, "C3_mean": c3, "C3": c3 >= MARGIN}
        lines.append(f"| {view} ({len(seeds)}) | " + " | ".join(f"{table[r].mean():.3f}" for r in RECIPES)
                     + " | " + " | ".join(cell(contrasts[f"{a} - {b}"]) for a, b in PAIRS) + " |")
    ok = all(out.get(v, {}).get("C3", False) for v in VIEWS)
    lines += ["", f"C3 preservation (keep_pred - founder at or above {MARGIN} on every view): "
              f"{'met' if ok else 'missed'}", ""]
    out["C3"] = ok
    return lines, out


def p1(runs: Path) -> tuple[list[str], dict[str, Any]]:
    found = bodies(runs, "p1")
    seeds = sorted(set.intersection(*(set(found[r]) for r in RECIPES)))
    if not seeds:
        return ["## P1: no founder read under every recipe", ""], {}
    lines = [f"## P1, founders {seeds[0]} to {seeds[-1]} ({len(seeds)})", ""] + head("Arm, reading")
    out: dict[str, Any] = {"seeds": seeds}
    gate = True
    for arm in P1_ARMS:
        for label, read in P1_READINGS:
            values = {r: [read(found[r][s]["arms"][arm]) for s in seeds] for r in RECIPES}
            if any(v is None for r in RECIPES for v in values[r]):
                continue
            contrasts = {f"{a} - {b}": paired_bootstrap(values[a], values[b]) for a, b in PAIRS}
            out.setdefault(arm, {})[label] = {"values": values, "contrasts": contrasts}
            if label == "sampled after teaching":
                gate = gate and contrasts["keep_pred - founder"]["bootstrap_95"][1] >= 0
            lines.append(f"| {arm}, {label} | " + " | ".join(f"{np.mean(values[r]):.3f}" for r in RECIPES)
                         + " | " + " | ".join(cell(contrasts[f"{a} - {b}"]) for a, b in PAIRS) + " |")
    out["gate"] = gate
    lines += ["", f"P1 gate (keep_pred - founder, every arm's upper interval end at or above zero): "
              f"{'met' if gate else 'missed'}", ""]
    return lines, out


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    runs = Path(argv[0])
    s_lines, s_out = screen(runs)
    p_lines, p_out = p1(runs)
    lines = ["# The recall memory kept across episodes and keyed by its predecessor", ""] + s_lines + p_lines
    (runs / "CONTINUING_RESULTS.md").write_text("\n".join(lines) + "\n")
    (runs / "continuing-summary.json").write_text(json.dumps({"screen": s_out, "p1": p_out}, indent=1,
                                                             default=float) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
