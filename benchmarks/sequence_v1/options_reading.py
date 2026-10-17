"""The recall memory's four options on the context-key screen and on P1
(``protocol-options-screen.json``, ``protocol-options-p1.json``): read the runs.

    python options_reading.py RUNS   # OPTIONS_RESULTS.md and options-summary.json in RUNS

``RUNS`` holds ``screen-<view>/s<seed>/<recipe>/founder-<seed>/founder.json`` and
``p1/s<seed>/<recipe>/founder-<seed>/founder.json``: one runner process per view (or P1) and
founder, every recipe in each. The criteria are the protocols' S1 (preservation on every
view), S2 (the P1 gate) and S3 (the options against the pull request's memory); the intervals
are percentile bootstraps over founders (``metrics.paired_bootstrap``), each founder's arms
averaged on the screen.
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
RECIPES = ("founder", "recall", "aroused", "rewarded", "improved")
SCREEN_ARMS = rs.ARMS
P1_ARMS = ("natural_step", "grade_step", "correct_step", "correct_step_qualified", "natural_live",
           "grade_live")
PAIRS = (("improved", "founder"), ("recall", "founder"), ("improved", "recall"), ("aroused", "recall"),
         ("rewarded", "recall"))
MARGIN = -0.05
P1_READINGS = (("sampled after teaching", lambda a: rs.sampled(a)),
               ("greedy after teaching", lambda a: rs.greedy(a)),
               ("sampled after the episodes alone", lambda a: rs.sampled(a, "withdrawn")),
               ("greedy after the episodes alone", lambda a: rs.greedy(a, "withdrawn")))


def bodies(runs: Path, reading: str) -> dict[str, dict[int, dict[str, Any]]]:
    out: dict[str, dict[int, dict[str, Any]]] = {recipe: {} for recipe in RECIPES}
    for part in sorted((runs / reading).glob("s*")):
        for recipe in RECIPES:
            out[recipe].update(rs.founder_files(part, recipe))
    return out


def common(found: dict[str, dict[int, dict[str, Any]]]) -> list[int]:
    seeds = set.intersection(*(set(found[recipe]) for recipe in RECIPES))
    return sorted(seeds)


def cell(c: dict[str, Any]) -> str:
    low, high = c["bootstrap_95"]
    signs = f"{c['positive']}/{c['negative']}/{c['zero']}"
    return f"{c['mean_difference']:+.3f} [{low:+.3f}, {high:+.3f}] ({signs})"


def screen(runs: Path) -> tuple[list[str], dict[str, Any]]:
    lines = ["## The screen", "",
             "Sampled success, recipe means over founders and arms; paired differences with the "
             "founder-resampled 95% interval and the founders up / down / equal.", "",
             "| View | Founders | founder | recall | aroused | rewarded | improved | "
             "improved - founder (S1) | recall - founder | improved - recall | aroused - recall | "
             "rewarded - recall | S1 |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    out: dict[str, Any] = {}
    for view in VIEWS:
        found = bodies(runs, f"screen-{view}")
        seeds = common(found)
        if not seeds:
            lines.append(f"| {view} | 0 | | | | | | | | | | | missing |")
            continue
        table = {recipe: np.array([[rs.sampled(found[recipe][s]["arms"][arm]) for arm in SCREEN_ARMS]
                                   for s in seeds], dtype=float) for recipe in RECIPES}
        per_founder = {recipe: table[recipe].mean(axis=1) for recipe in RECIPES}
        contrasts = {f"{a} - {b}": paired_bootstrap(per_founder[a], per_founder[b]) for a, b in PAIRS}
        s1 = float((table["improved"] - table["founder"]).mean())
        clean = {recipe: int(sum(bool(rs.clean(found[recipe][s]["arms"][arm])) for s in seeds
                                 for arm in SCREEN_ARMS)) for recipe in RECIPES}
        kinds = {kind: {f"{a} - {b}": paired_bootstrap(
            table[a][:, [SCREEN_ARMS.index(x) for x in arms]].mean(axis=1),
            table[b][:, [SCREEN_ARMS.index(x) for x in arms]].mean(axis=1)) for a, b in PAIRS}
            for kind, arms in rs.KINDS.items()}
        out[view] = {"founders": seeds, "means": {r: float(table[r].mean()) for r in RECIPES},
                     "contrasts": contrasts, "kinds": kinds, "clean_passes": clean,
                     "S1_mean": s1, "S1": s1 >= MARGIN,
                     "per_founder": {r: per_founder[r].tolist() for r in RECIPES}}
        lines.append(
            f"| {view} | {len(seeds)} | " + " | ".join(f"{table[r].mean():.3f}" for r in RECIPES)
            + " | " + " | ".join(cell(contrasts[f"{a} - {b}"]) for a, b in PAIRS)
            + f" | {'met' if s1 >= MARGIN else 'missed'} |")
    lines += ["", "Clean greedy passes (of founders x arms), per recipe:", "",
              "| View | " + " | ".join(RECIPES) + " |", "| --- |" + " --- |" * len(RECIPES)]
    for view in VIEWS:
        if view in out:
            lines.append(f"| {view} | " + " | ".join(str(out[view]["clean_passes"][r]) for r in RECIPES)
                         + " |")
    lines += ["", "Per arm kind (place, ctx5), paired differences:", "",
              "| View | Kind | " + " | ".join(f"{a} - {b}" for a, b in PAIRS) + " |",
              "| --- | --- |" + " --- |" * len(PAIRS)]
    for view in VIEWS:
        if view in out:
            for kind in rs.KINDS:
                lines.append(f"| {view} | {kind} | " + " | ".join(
                    cell(out[view]["kinds"][kind][f"{a} - {b}"]) for a, b in PAIRS) + " |")
    s1_all = all(out.get(view, {}).get("S1", False) for view in VIEWS)
    lines += ["", f"S1 preservation over the screen: {'met' if s1_all else 'missed'} "
              f"(every view's mean of improved - founder at or above {MARGIN})", ""]
    out["S1"] = s1_all
    return lines, out


def p1(runs: Path) -> tuple[list[str], dict[str, Any]]:
    found = bodies(runs, "p1")
    seeds = common(found)
    if not seeds:
        return ["## P1: no founder read under every recipe", ""], {}
    lines = [f"## P1, founders {seeds[0]} to {seeds[-1]} ({len(seeds)})", "",
             "| Arm | Reading | founder | recall | aroused | rewarded | improved | improved - founder | "
             "recall - founder | improved - recall | aroused - recall | rewarded - recall |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    out: dict[str, Any] = {"seeds": seeds}
    gate = True
    for arm in P1_ARMS:
        out[arm] = {}
        for label, read in P1_READINGS:
            values = {r: [read(found[r][s]["arms"][arm]) for s in seeds] for r in RECIPES}
            if any(v is None for r in RECIPES for v in values[r]):
                continue
            contrasts = {f"{a} - {b}": paired_bootstrap(values[a], values[b]) for a, b in PAIRS}
            out[arm][label] = {"values": values, "contrasts": contrasts}
            if label == "sampled after teaching":
                upper = contrasts["improved - founder"]["bootstrap_95"][1]
                out[arm]["S2"] = upper >= 0
                gate = gate and upper >= 0
            lines.append(f"| {arm} | {label} | " + " | ".join(f"{np.mean(values[r]):.3f}" for r in RECIPES)
                         + " | " + " | ".join(cell(contrasts[f"{a} - {b}"]) for a, b in PAIRS) + " |")
    controls = {name: float(np.mean([rs.sampled(found["founder"][s]["arms"][name]) for s in seeds]))
                for name in ("random", "searcher", "founder")}
    out["controls"], out["S2"] = controls, gate
    lines += ["", f"Controls (founder recipe): random {controls['random']:.3f}, searcher "
              f"{controls['searcher']:.3f}, untrained founder {controls['founder']:.3f}", "",
              f"S2, the P1 gate (every arm's upper interval end of improved - founder in sampled "
              f"success after teaching at or above zero): {'met' if gate else 'missed'}", ""]
    return lines, out


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    runs = Path(argv[0])
    lines = ["# The recall memory's four options on the Stone Age chambers", ""]
    screen_lines, screen_out = screen(runs)
    p1_lines, p1_out = p1(runs)
    lines += screen_lines + p1_lines
    (runs / "OPTIONS_RESULTS.md").write_text("\n".join(lines) + "\n")
    (runs / "options-summary.json").write_text(json.dumps({"screen": screen_out, "p1": p1_out},
                                                          indent=1, default=float) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
