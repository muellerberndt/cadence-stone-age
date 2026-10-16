"""The recall-memory witness (RECALL_PROTOCOL.md): derive the per-view protocols from the
master declaration, and read the runs.

    python recall_screen.py derive                      # protocol-recall-screen-<view>.json
    python recall_screen.py analyze RUNS [CONTROL_RUNS] # RECALL_RESULTS.md and recall-summary.json

``derive`` writes one runnable protocol per entry of the master's ``views``: the master's
``world`` with that view and its note, the master's name with the view named, everything else
unchanged. ``analyze`` reads ``RUNS/rs-<view>/<recipe>/founder-<seed>/founder.json`` and
``RUNS/rs-p1*/...`` (founder 1001 and the extension founders' runs) and, when ``CONTROL_RUNS`` is given, checks the founder recipe against the
dense founder's earlier control runs there (``sk-control-<view>/sensory``, ``sk-control-p1``).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
MASTER = HERE / "protocol-recall-screen.json"
VIEW_TITLES = {
    "hidden": "progress hidden (A, B, A, B)",
    "invisible": "an invisible step (A, A, B, C)",
    "visible": "progress visible (V5's own observations)",
    "consecutive": "two consecutive aliases (A, A, B, B)",
}
RECIPES = ("founder", "recall")
ARMS = ("place_natural_120", "place_corrective_120", "ctx5_natural_120", "ctx5_corrective_120")
KINDS = {"place": ("place_natural_120", "place_corrective_120"),
         "ctx5": ("ctx5_natural_120", "ctx5_corrective_120")}
MARGIN = -0.05


def derive() -> list[Path]:
    master = json.loads(MASTER.read_text())
    out = []
    for view in master["views"]:
        protocol = {k: v for k, v in master.items() if k != "views"}
        world = {k: v for k, v in master["world"].items() if k not in ("view", "notes")}
        world["view"] = view
        world["note"] = master["world"]["notes"][view]
        protocol["world"] = world
        protocol["name"] = (f"The recall memory, {VIEW_TITLES[view]}: Brain.compose(..., recall=True) "
                            "at the founder genes against the founder with it off")
        protocol["derived_from"] = {"file": MASTER.name, "view": view,
                                    "note": "written by recall_screen.py derive; the master declares all four views"}
        path = HERE / f"protocol-recall-screen-{view}.json"
        path.write_text(json.dumps(protocol, indent=2) + "\n")
        out.append(path)
    return out


# -- reading the runs


def founder_files(run: Path, recipe: str) -> dict[int, dict[str, Any]]:
    out = {}
    for path in sorted(run.glob(f"{recipe}/founder-*/founder.json")):
        body = json.loads(path.read_text())
        out[int(body["seed"])] = body
    return out


def sampled(arm: dict[str, Any], phase: str = "frozen") -> float | None:
    reading = (arm.get(phase, {}) if phase == "frozen" else arm.get("withdrawal", {}).get("frozen", {}))
    return reading.get("sampled", {}).get("summary", {}).get("success_rate")


def greedy(arm: dict[str, Any], phase: str = "frozen") -> float | None:
    reading = (arm.get(phase, {}) if phase == "frozen" else arm.get("withdrawal", {}).get("frozen", {}))
    return reading.get("greedy", {}).get("summary", {}).get("success_rate")


def clean(arm: dict[str, Any], phase: str = "frozen") -> bool | None:
    reading = (arm.get(phase, {}) if phase == "frozen" else arm.get("withdrawal", {}).get("frozen", {}))
    summary = reading.get("greedy", {}).get("summary")
    if not summary or not summary.get("episodes"):
        return None
    return summary["exact_minimal_completions"] == summary["episodes"]


def first_try(arm: dict[str, Any]) -> list[float | None] | None:
    return arm.get("frozen", {}).get("sampled", {}).get("summary", {}).get("first_try_accuracy")


def per_state(arm: dict[str, Any], phase: str = "trained") -> float | None:
    entry = arm.get("per_state") if phase == "trained" else arm.get("withdrawal", {}).get("per_state")
    if not entry:
        return None
    name = "chain" if "chain" in entry else next(iter(entry))
    return entry[name]["accuracy"]


def mean_sem(values: list[float]) -> tuple[float, float]:
    a = np.asarray(values, dtype=float)
    sem = float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan")
    return float(a.mean()), sem


def screen(runs: Path, views: list[str]) -> tuple[list[str], dict[str, Any]]:
    lines: list[str] = []
    summary: dict[str, Any] = {}
    verdict: dict[str, bool | None] = {}
    benefit: dict[str, bool | None] = {}
    for view in views:
        run = runs / f"rs-{view}"
        if not run.exists():
            lines += [f"## {view}: no run directory", ""]
            verdict[view] = benefit[view] = None
            continue
        bodies = {recipe: founder_files(run, recipe) for recipe in RECIPES}
        seeds = sorted(set(bodies["founder"]) & set(bodies["recall"]))
        lines += [f"## {view}: {VIEW_TITLES[view]}", "",
                  "| arm | founder | sampled founder | sampled recall | diff | clean founder | clean recall | "
                  "first try founder | first try recall |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        pairs: dict[str, list[tuple[float, float, bool | None, bool | None]]] = {}
        for arm in ARMS:
            for seed in seeds:
                a = bodies["recall"][seed]["arms"][arm]
                b = bodies["founder"][seed]["arms"][arm]
                sa, sb = sampled(a), sampled(b)
                ca, cb = clean(a), clean(b)
                pairs.setdefault(arm, []).append((sa, sb, ca, cb))
                fa, fb = first_try(a) or [], first_try(b) or []
                lines.append(f"| {arm} | {seed} | {sb:.2f} | {sa:.2f} | {sa - sb:+.2f} | {int(bool(cb))} | {int(bool(ca))} | "
                             f"{' '.join('-' if v is None else f'{v:.2f}' for v in fb)} | "
                             f"{' '.join('-' if v is None else f'{v:.2f}' for v in fa)} |")
        lines.append("")
        controls = {}
        for name in ("random", "searcher", "founder"):
            values = [sampled(bodies["founder"][seed]["arms"][name]) for seed in seeds]
            controls[name] = float(np.mean(values))
        lines.append(f"Controls (founder recipe, mean over founders): random {controls['random']:.3f}, "
                     f"searcher {controls['searcher']:.3f}, untrained founder {controls['founder']:.3f}; "
                     f"untrained recall founder {np.mean([sampled(bodies['recall'][s]['arms']['founder']) for s in seeds]):.3f}")
        lines.append("")
        lines += ["| pairs | n | sampled founder | sampled recall | diff (SEM) | up / down / equal | clean founder | clean recall | discordant recall-only / founder-only |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        entry: dict[str, Any] = {"seeds": seeds, "controls": controls}

        def row(label: str, items: list[tuple[float, float, bool | None, bool | None]]) -> dict[str, Any]:
            diffs = [a - b for a, b, _, _ in items]
            mean, sem = mean_sem(diffs)
            up = sum(1 for d in diffs if d > 0)
            down = sum(1 for d in diffs if d < 0)
            ca = sum(1 for _, _, c, _ in items if c)
            cb = sum(1 for _, _, _, c in items if c)
            only_a = sum(1 for _, _, c, d in items if c and not d)
            only_b = sum(1 for _, _, c, d in items if d and not c)
            lines.append(f"| {label} | {len(items)} | {np.mean([b for _, b, _, _ in items]):.3f} | "
                         f"{np.mean([a for a, _, _, _ in items]):.3f} | {mean:+.3f} ({sem:.3f}) | "
                         f"{up} / {down} / {len(items) - up - down} | {cb} | {ca} | {only_a} / {only_b} |")
            return {"pairs": len(items), "sampled_founder": float(np.mean([b for _, b, _, _ in items])),
                    "sampled_recall": float(np.mean([a for a, _, _, _ in items])), "diff": mean, "sem": sem,
                    "up": up, "down": down, "clean_founder": cb, "clean_recall": ca,
                    "discordant_recall_only": only_a, "discordant_founder_only": only_b}

        for kind, arms in KINDS.items():
            entry[kind] = row(kind, [p for arm in arms for p in pairs[arm]])
        entry["all"] = row("all", [p for arm in ARMS for p in pairs[arm]])
        verdict[view] = entry["all"]["diff"] >= MARGIN
        benefit[view] = entry["all"]["diff"] > 0
        lines += ["", f"Preservation on this view (all pairs at or above {MARGIN:+.2f} in sampled success): "
                  f"{'met' if verdict[view] else 'missed'}; recall above the founder: {'yes' if benefit[view] else 'no'}", ""]
        summary[view] = entry
    summary["preservation"] = verdict
    summary["preserved_every_view"] = all(v is True for v in verdict.values())
    summary["benefit_views"] = [v for v, b in benefit.items() if b]
    return lines, summary


def p1(runs: Path) -> tuple[list[str], dict[str, Any]]:
    parts = sorted(runs.glob("rs-p1*"))  # founder 1001's run and the extension founders' runs
    if not parts:
        return ["## P1: no run directory", ""], {}
    bodies: dict[str, dict[int, dict[str, Any]]] = {recipe: {} for recipe in RECIPES}
    for run in parts:
        for recipe in RECIPES:
            bodies[recipe].update(founder_files(run, recipe))
    seeds = sorted(set(bodies["founder"]) & set(bodies["recall"]))
    if not seeds:
        return ["## P1: no founder read under both recipes", ""], {}
    arms = [a for a in bodies["founder"][seeds[0]]["arms"] if a not in ("founder", "random", "oracle", "searcher")]
    lines = [f"## P1 (cold chain, fully observed), founders {', '.join(map(str, seeds))}", "",
             "| arm | reading | founder | recall | diff |", "| --- | --- | --- | --- | --- |"]
    out: dict[str, Any] = {"seeds": seeds}
    readings = (("sampled after teaching", lambda a: sampled(a)), ("greedy after teaching", lambda a: greedy(a)),
                ("per-state after teaching", lambda a: per_state(a)),
                ("sampled after 80 alone", lambda a: sampled(a, "withdrawn")),
                ("greedy after 80 alone", lambda a: greedy(a, "withdrawn")),
                ("per-state after 80 alone", lambda a: per_state(a, "withdrawn")))
    for arm in arms:
        out[arm] = {}
        for label, read in readings:
            va = [read(bodies["recall"][s]["arms"][arm]) for s in seeds]
            vb = [read(bodies["founder"][s]["arms"][arm]) for s in seeds]
            if any(v is None for v in va + vb):
                continue
            diff = float(np.mean(va) - np.mean(vb))
            cell = f"{diff:+.3f}"
            if len(seeds) >= 2:
                from metrics import paired_bootstrap  # noqa: PLC0415

                c = paired_bootstrap(va, vb)
                cell += f" [{c['bootstrap_95'][0]:+.3f}, {c['bootstrap_95'][1]:+.3f}]"
            lines.append(f"| {arm} | {label} | {np.mean(vb):.3f} | {np.mean(va):.3f} | {cell} |")
            out[arm][label] = {"founder": [float(v) for v in vb], "recall": [float(v) for v in va], "diff": diff}
    controls = {name: float(np.mean([sampled(bodies["founder"][s]["arms"][name]) for s in seeds]))
                for name in ("random", "searcher", "founder")}
    lines += ["", f"Controls (founder recipe): random {controls['random']:.3f}, searcher {controls['searcher']:.3f}, "
              f"untrained founder {controls['founder']:.3f}", ""]
    out["controls"] = controls
    return lines, out


def strip(value: Any) -> Any:
    """An arm's record without its wall seconds and without the event digest, which covers the
    life id (``<recipe>/<seed>/<arm>/train``) and so differs between recipe names; the event
    streams are compared on their own with the life id removed."""
    if isinstance(value, dict):
        return {k: strip(v) for k, v in value.items() if k not in ("seconds", "events_sha256")}
    if isinstance(value, list):
        return [strip(v) for v in value]
    return value


def events_equal(mine: Path, other: Path) -> bool | None:
    """Whether two event logs hold the same events once the life id is removed."""
    import gzip  # noqa: PLC0415

    if not mine.exists() or not other.exists():
        return None
    a = [json.loads(line) for line in gzip.open(mine, "rt")]
    b = [json.loads(line) for line in gzip.open(other, "rt")]
    for event in a + b:
        event.pop("life", None)
    return a == b


def control_check(runs: Path, control: Path, views: list[str]) -> tuple[list[str], dict[str, Any]]:
    """The founder recipe against the dense founder's earlier control runs, arm for arm: every
    arm record (readings, digests, counts) and every training and withdrawal event stream."""
    lines = ["## Control check: the founder recipe against the earlier dense-founder runs", "",
             "| run | founder | founder digest same | arms compared | different records | event streams equal (life id removed) |",
             "| --- | --- | --- | --- | --- | --- |"]
    report: dict[str, Any] = {}
    same_all = True
    pairs = [(f"rs-{view}", f"sk-control-{view}") for view in views]
    pairs += [(run.name, "sk-control-p1") for run in sorted(runs.glob("rs-p1*"))]
    for rerun, original in pairs:
        for seed, body in founder_files(runs / rerun, "founder").items():
            path = control / original / "sensory" / f"founder-{seed}" / "founder.json"
            if not path.exists() and original == "sk-control-p1":
                # the extension founders: the earlier lane's full P1 run of the dense founder
                path = control / "ck-p1" / "sensory" / f"founder-{seed}" / "founder.json"
            if not path.exists():
                lines.append(f"| {rerun} | {seed} | no control file | - | - | - |")
                report[f"{rerun}/{seed}"] = {"control": None}
                continue
            other = json.loads(path.read_text())
            arms = sorted(set(body["arms"]) | set(other["arms"]))
            different = [arm for arm in arms if strip(body["arms"].get(arm)) != strip(other["arms"].get(arm))]
            same = body["founder_digest"] == other["founder_digest"]
            streams: dict[str, bool | None] = {}
            for log in sorted(path.parent.glob("*-events.jsonl.gz")):
                streams[log.name] = events_equal(runs / rerun / "founder" / f"founder-{seed}" / log.name, log)
            equal = sum(1 for v in streams.values() if v)
            same_all &= same and not different and equal == len(streams) > 0
            report[f"{rerun}/{seed}"] = {"founder_digest_same": same, "arms": len(arms), "different": different,
                                         "event_streams": streams}
            lines.append(f"| {rerun} | {seed} | {same} | {len(arms)} | {different or 'none'} | {equal} of {len(streams)} |")
    report["all_same"] = same_all
    lines += ["", f"All readings, digests and event streams equal the control runs: {same_all}", ""]
    return lines, report


def analyze(runs: Path, control: Path | None) -> int:
    master = json.loads(MASTER.read_text())
    views = master["views"]
    lines = ["# The recall memory on the Stone Age chambers: results", "",
             f"Runs under `{runs}`; readings as declared in RECALL_PROTOCOL.md. Sampled success is the share of 100 "
             "frozen episodes completed within 10 decisions; a clean pass is the one greedy episode completed in four "
             "decisions; diff is recall minus founder, paired by founder and arm.", ""]
    screen_lines, summary = screen(runs, views)
    lines += screen_lines
    lines += ["## Verdicts", "",
              f"- Preservation (every view's paired mean in sampled success at or above {MARGIN:+.2f}): "
              f"{'met' if summary['preserved_every_view'] else 'missed'}; per view {summary['preservation']}",
              f"- Benefit (views where recall exceeds the founder in sampled success): {summary['benefit_views'] or 'none'}", ""]
    p1_lines, p1_summary = p1(runs)
    lines += p1_lines
    summary["p1"] = p1_summary
    if control is not None:
        check_lines, check = control_check(runs, control, views)
        lines += check_lines
        summary["control_check"] = check
    (runs / "RECALL_RESULTS.md").write_text("\n".join(lines) + "\n")
    (runs / "recall-summary.json").write_text(json.dumps(summary, indent=1))
    print("\n".join(lines))
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in ("derive", "analyze"):
        print(__doc__)
        return 2
    if argv[0] == "derive":
        for path in derive():
            print(path.name)
        return 0
    runs = Path(argv[1]).resolve()
    control = Path(argv[2]).resolve() if len(argv) > 2 else None
    return analyze(runs, control)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
