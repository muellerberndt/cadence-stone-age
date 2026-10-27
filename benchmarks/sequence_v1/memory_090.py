"""The Cadence 0.90.0 candidate against 0.89.0 on the two worlds where the position term matters.

    python memory_090.py derive            # write protocol-m090-recall-order.json and -route-hidden.json
    python memory_090.py jobs OUT          # one line per runner process: library, reading, recipe, seed
    python memory_090.py analyze OUT       # paired tables -> OUT/M090_RESULTS.md, OUT/m090-summary.json
    python memory_090.py derive-diagnostic # protocol-m090d-*.json: one 0.89.0 setting restored at a time
    python memory_090.py jobs-diagnostic DIAG
    python memory_090.py analyze-diagnostic OUT DIAG   # -> DIAG/M090_DIAGNOSTIC.md

Readings: the ordered recall world taught (``teach_step``, as grid 5) and the route cue shown once
and hidden behind two neutral events, guided (``guide_step``, as grid 2). Recipes ``recall`` and
``recall_h2``, founders 1101 to 1120, which no earlier reading used. Each recipe runs on every
founder under both libraries, and every comparison pairs the two libraries on the same founder,
recipe and arm.

The libraries: ``R089``, the published ``cadence-net==0.89.0`` wheel; ``C090``, the 0.90.0
candidate (cadence source at commit 838bb49): every recall head's position term adds a learned
slope over age beside its bucket table, the table is exact to 64 ages and taught at the address
rate, the founder recency is 0, and a composed recall brain is taught by surprise. A recipe's
compose call is the same under both; each library brings its own founders.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from memory_089 import CHAIN_RECIPES, ORDER_RECIPES, bootstrap, conditions_of, read_run, recipes

HERE = Path(__file__).resolve().parent
SEEDS = list(range(1101, 1121))
WHEEL_0890 = "7b27009d0affd2235026ca5f7b4776ba545c15d5c5a14a61c75e52b6df65b786"
LIBRARIES = ("R089", "C090")
RECIPES = ("recall", "recall_h2")
# reading: protocol, the arm read, the protocol it is derived from
READINGS = {
    "recall-order": ("protocol-m090-recall-order.json", "teach_step", "protocol-m089e-recall-order.json"),
    "route-hidden": ("protocol-m090-route-hidden.json", "guide_step", "protocol-m089b-route-hidden.json"),
}
GATE = -0.03  # the paired mean difference C090 - R089 a recipe may not fall below


def derive() -> list[str]:
    """The two protocols: the grid-5 and grid-2 protocols with the new founders; the route protocol
    also carries grid 1's ``recall`` recipe, which grid 2 did not run."""
    written = []
    p = json.loads((HERE / READINGS["recall-order"][2]).read_text())
    p["name"] = "Cadence 0.90 candidate against 0.89.0 on the ordered recall world: 20 fresh founders"
    p["scope"] = "component reading of a library release in a world; confirmation founders"
    p["recipes"] = recipes(ORDER_RECIPES, p["recipes"]["carried"]["compose"])
    p["seeds"] = {"development": SEEDS}
    (HERE / READINGS["recall-order"][0]).write_text(json.dumps(p, indent=1) + "\n")
    written.append(READINGS["recall-order"][0])
    p = json.loads((HERE / READINGS["route-hidden"][2]).read_text())
    p["name"] = "Cadence 0.90 candidate against 0.89.0 on the route cue, cue hidden: 20 fresh founders"
    p["scope"] = "component reading of a library release in a world; confirmation founders"
    base = p["recipes"]["defaults"]["compose"]
    p["recipes"]["recall"] = recipes({"recall": CHAIN_RECIPES["recall"]}, base)["recall"]
    p["seeds"] = {"development": SEEDS}
    (HERE / READINGS["route-hidden"][0]).write_text(json.dumps(p, indent=1) + "\n")
    written.append(READINGS["route-hidden"][0])
    return written


def jobs(out: Path) -> None:
    lines = []
    for reading in READINGS:  # the longer ordered-recall lives first
        protocol, arm, _ = READINGS[reading]
        for seed in SEEDS:
            for recipe in RECIPES:
                for library in LIBRARIES:  # the two libraries of a pair side by side
                    lines.append(f"{library} {reading} {protocol} {recipe} {seed} {arm}")
    (out / "jobs.txt").write_text("\n".join(lines) + "\n")
    print(len(lines), "jobs")


def library_of(run: Path) -> dict:
    """The version and package digest (of its ``*.py`` files) the run's manifest records."""
    manifest = json.loads((run / "manifest.json").read_text())
    cadence = manifest["cadence"]
    return {"version": cadence["version"], "package": cadence["package"]["digest"],
            "wheel_sha256": cadence["wheel_sha256"], "seconds": manifest.get("wall_seconds")}


def analyze(out: Path) -> None:
    summary: dict = {"gate": GATE, "readings": {}}
    lines = ["# Cadence 0.90 candidate against 0.89.0 (founders 1101 to 1120)", "",
             "Frozen success, sampled (greedy), mean over founders; the difference C090 - R089 is "
             "founder-paired, bootstrap 95% (10,000 resamples, seed 31012).", ""]
    libraries: dict = {}
    for reading, (_, arm, _) in READINGS.items():
        lines += [f"## {reading} ({arm})", "",
                  "| Recipe | Founders | R089 | C090 | C090 - R089 [95%] | Up/down | Gate |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        summary["readings"][reading] = {"arm": arm, "recipes": {}}
        for recipe in RECIPES:
            rows = {}
            for seed in SEEDS:
                runs = {lib: out / lib / reading / recipe / f"s{seed}" for lib in LIBRARIES}
                read = {lib: read_run(path, recipe) for lib, path in runs.items()}
                if any(r is None for r in read.values()):
                    continue
                rows[seed] = {lib: read[lib][arm] for lib in LIBRARIES}
                for lib, path in runs.items():
                    ident = library_of(path)
                    libraries.setdefault(lib, set()).add((ident["version"], ident["package"]))
                    rows[seed][lib]["seconds"] = ident["seconds"]
                    if reading == "recall-order":
                        rows[seed][lib]["conditions"] = conditions_of(path).get(arm, {})
            if not rows:
                continue
            seeds = sorted(rows)
            sampled = {lib: np.array([rows[s][lib]["sampled"] for s in seeds]) for lib in LIBRARIES}
            greedy = {lib: np.array([rows[s][lib]["greedy"] for s in seeds]) for lib in LIBRARIES}
            diffs = sampled["C090"] - sampled["R089"]
            lo, hi = bootstrap(diffs)
            up, down = int((diffs > 0).sum()), int((diffs < 0).sum())
            passed = bool(diffs.mean() >= GATE)
            entry = {
                "founders": len(seeds),
                **{lib: {"sampled": float(sampled[lib].mean()), "greedy": float(greedy[lib].mean()),
                         "per_founder": {str(s): rows[s][lib]["sampled"] for s in seeds},
                         "seconds": float(np.mean([rows[s][lib]["seconds"] or 0.0 for s in seeds]))}
                   for lib in LIBRARIES},
                "difference": float(diffs.mean()), "ci": [lo, hi], "up": up, "down": down,
                "passed": passed,
            }
            if reading == "recall-order":
                for lib in LIBRARIES:
                    names = sorted({c for s in seeds for c in rows[s][lib]["conditions"]})
                    entry[lib]["conditions"] = {
                        c: float(np.mean([rows[s][lib]["conditions"][c] for s in seeds
                                          if c in rows[s][lib]["conditions"]])) for c in names}
            summary["readings"][reading]["recipes"][recipe] = entry
            lines.append(
                f"| {recipe} | {len(seeds)} | {entry['R089']['sampled']:.3f} ({entry['R089']['greedy']:.2f}) | "
                f"{entry['C090']['sampled']:.3f} ({entry['C090']['greedy']:.2f}) | "
                f"{entry['difference']:+.3f} [{lo:+.3f}, {hi:+.3f}] | {up}/{down} | "
                f"{'passes' if passed else 'fails'} |")
        lines.append("")
        if reading == "recall-order":
            lines += ["Per condition, sampled (the first or the latest written value asked; adjacent writes "
                      "or one neutral event between them):", "",
                      "| Recipe | Library | " + " | ".join(
                          sorted({c for e in summary["readings"][reading]["recipes"].values()
                                  for c in e["R089"].get("conditions", {})})) + " |"]
            names = sorted({c for e in summary["readings"][reading]["recipes"].values()
                            for c in e["R089"].get("conditions", {})})
            lines.append("| --- | --- | " + " | ".join("---" for _ in names) + " |")
            for recipe, entry in summary["readings"][reading]["recipes"].items():
                for lib in LIBRARIES:
                    cond = entry[lib].get("conditions", {})
                    lines.append(f"| {recipe} | {lib} | " + " | ".join(
                        f"{cond[c]:.2f}" if c in cond else "" for c in names) + " |")
            lines.append("")
    summary["libraries"] = {lib: sorted(list(v)) for lib, v in libraries.items()}
    every = [e["passed"] for r in summary["readings"].values() for e in r["recipes"].values()]
    summary["passed"] = bool(every) and all(every)
    lines += ["Libraries as the runs' manifests record them (version, package digest):", ""]
    for lib, idents in summary["libraries"].items():
        for version, package in idents:
            lines.append(f"- {lib}: {version}, `{package}`")
    lines += ["", f"Gate: the paired mean difference at least {GATE} for each recipe on each world: "
              f"**{'passes' if summary['passed'] else 'fails'}**.", ""]
    (out / "m090-summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    (out / "M090_RESULTS.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


# -- a diagnostic after the readings: which change of the candidate moves the result

# Each recipe takes the candidate's ``recall`` recipe back to one 0.89.0 setting; ``recall_089``
# takes it back to all of them, so under the candidate it must read as ``recall`` under 0.89.0.
DIAG_EXTRA = {
    "recall_every": ({"learning_surprise": False}, "lessons on every row (0.89.0's default)"),
    "recall_r025": ({"recall_recency": 0.25}, "the age charge of 0.25 (0.89.0's founder)"),
    "recall_p32": ({"recall_position": 32, "recall_position_rate": 0.1, "recall_slope_rate": 0.0},
                   "0.89.0's position term: 32 exact ages at rate 0.1, no slope"),
    "recall_089": ({"learning_surprise": False, "recall_recency": 0.25, "recall_position": 32,
                    "recall_position_rate": 0.1, "recall_slope_rate": 0.0}, "every 0.89.0 setting"),
}
DIAG = {reading: (f"protocol-m090d-{reading}.json", arm) for reading, (_, arm, _) in READINGS.items()}


def derive_diag() -> list[str]:
    written = []
    for reading, (protocol, _) in DIAG.items():
        p = json.loads((HERE / READINGS[reading][0]).read_text())
        p["name"] = p["name"].replace("Cadence 0.90 candidate against 0.89.0", "Diagnostic of the 0.90 candidate")
        base = p["recipes"]["recall"]["compose"]
        p["recipes"] = {"recall": p["recipes"]["recall"], **recipes(DIAG_EXTRA, base)}
        (HERE / protocol).write_text(json.dumps(p, indent=1) + "\n")
        written.append(protocol)
    return written


def jobs_diag(out: Path) -> None:
    lines = [f"C090 {reading} {protocol} {recipe} {seed} {arm}"
             for reading, (protocol, arm) in DIAG.items() for seed in SEEDS for recipe in DIAG_EXTRA]
    (out / "jobs.txt").write_text("\n".join(lines) + "\n")
    print(len(lines), "jobs")


def analyze_diag(readings: Path, out: Path) -> None:
    """Each diagnostic recipe under the candidate against ``recall`` under the candidate and under
    0.89.0 (from the readings in ``readings``), founder-paired."""
    lines = ["# Diagnostic of the 0.90 candidate (founders 1101 to 1120, after the readings)", "",
             "The candidate's `recall` recipe with one 0.89.0 setting restored at a time. Sampled frozen "
             "success, mean over founders; differences founder-paired, bootstrap 95%.", ""]
    summary: dict = {}
    for reading, (_, arm) in DIAG.items():
        def sampled(lib_dir: Path, recipe: str) -> dict:
            got = {}
            for seed in SEEDS:
                run = read_run(lib_dir / reading / recipe / f"s{seed}", recipe)
                if run is not None:
                    got[seed] = run[arm]["sampled"]
            return got
        cand = sampled(readings / "C090", "recall")
        old = sampled(readings / "R089", "recall")
        lines += [f"## {reading} ({arm})", "",
                  "| Recipe under the candidate | Sampled | - `recall` under the candidate [95%] | "
                  "- `recall` under 0.89.0 [95%] |", "| --- | --- | --- | --- |",
                  f"| `recall` (the candidate as composed) | {np.mean(list(cand.values())):.3f} | | |"]
        summary[reading] = {"recall_C090": float(np.mean(list(cand.values()))),
                            "recall_R089": float(np.mean(list(old.values())))}
        for recipe in DIAG_EXTRA:
            got = sampled(out / "C090", recipe)
            if not got:
                continue
            cells = []
            for ref in (cand, old):
                seeds = [s for s in got if s in ref]
                d = np.array([got[s] - ref[s] for s in seeds])
                lo, hi = bootstrap(d)
                cells.append(f"{d.mean():+.3f} [{lo:+.3f}, {hi:+.3f}]")
            summary[reading][recipe] = {"sampled": float(np.mean(list(got.values()))),
                                        "per_founder": {str(s): v for s, v in got.items()}}
            lines.append(f"| `{recipe}`: {DIAG_EXTRA[recipe][1]} | {np.mean(list(got.values())):.3f} | "
                         f"{cells[0]} | {cells[1]} |")
        lines += ["", f"`recall` under 0.89.0: {np.mean(list(old.values())):.3f}.", ""]
    (out / "m090d-summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    (out / "M090_DIAGNOSTIC.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "derive":
        print("\n".join(derive()))
    elif command == "jobs":
        jobs(Path(sys.argv[2]))
    elif command == "analyze":
        analyze(Path(sys.argv[2]))
    elif command == "derive-diagnostic":
        print("\n".join(derive_diag()))
    elif command == "jobs-diagnostic":
        jobs_diag(Path(sys.argv[2]))
    elif command == "analyze-diagnostic":
        analyze_diag(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        raise SystemExit(__doc__)
