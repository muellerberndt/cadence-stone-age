"""The memory of Cadence 0.89.0 on the chambers where context decides a later action.

    python memory_089.py derive              # write the protocol-m089-*.json files
    python memory_089.py jobs OUT            # one line per runner process: reading, recipe, seed
    python memory_089.py analyze OUT         # tables per reading, recipe and arm -> M089_RESULTS.md

Readings: the chain seen four ways (hidden A B A B, invisible A A B C, visible, consecutive A A
B B; the screen's founders 202001 to 202020), the route cue shown once and then hidden or kept
visible (founders 1001 to 1010), the recall world (the latest written value; founders 1001 to
1010) and P1, the cold chain with its life alone (founders 1001 to 1010). Recipes add the 0.89
memory options to one base per reading; the base itself is the control. Every recipe runs on
every founder of its reading, and every comparison pairs a recipe with the base on the same
founder and arm.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = {"modules": [48, 24], "arousal": True}
CHAIN_RECIPES = {
    "defaults": ({}, "the base: Brain.compose(7, 5, modules=(48, 24), arousal=True)"),
    "episodic": ({"memory_choice": True}, "the episodic memory votes in the choice"),
    "recall": ({"recall": True}, "the recall memory with its default position term (32 exact ages)"),
    "recall_nopos": ({"recall": True, "recall_position": 0}, "the recall memory without the position term"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "the recall memory read by two heads"),
    "recall_w2": ({"recall": True, "recall_window": 2}, "the recall memory keyed on the last two events"),
    "attention": ({"attention": True, "learned_code": 8},
                  "the learned-code contextual recipe (recall, window 2, learned code of 8 units)"),
    "episodic_recall": ({"memory_choice": True, "recall": True}, "the episodic vote and the recall memory"),
}
RECALL_WORLD_RECIPES = {
    "carried": ({}, "the recall world's own base recipe"),
    "retained": ({"working_memory_decay": 0.8}, "the base with a retained working trace"),
    "recall": ({"recall": True}, "the base with the recall memory and its default position term"),
    "recall_nopos": ({"recall": True, "recall_position": 0}, "the base with the recall memory, no position term"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "the base with two recall heads"),
    "attention": ({"attention": True, "learned_code": 8}, "the base with the learned-code contextual recipe"),
}
VIEW_ARMS = {
    "natural_step_120": {"adapter": "step", "caregiver": "none", "training_episodes": 120},
    "corrective_step_120": {"adapter": "step", "caregiver": "correct", "training_episodes": 120},
    "corrective_step_480": {"adapter": "step", "caregiver": "correct", "training_episodes": 480},
    "natural_live_480": {"adapter": "live", "caregiver": "none", "training_episodes": 480},
}
ROUTE_ARMS = {
    "guide_step": {"adapter": "step", "caregiver": "guide"},
    "grade_step": {"adapter": "step", "caregiver": "grade"},
    "natural_live": {"adapter": "live", "caregiver": "none"},
}
VIEW_SEEDS = list(range(202001, 202021))
SEEDS = list(range(1001, 1011))
VIEWS = ("hidden", "invisible", "visible", "consecutive")


def recipes(table: dict, base: dict) -> dict:
    out = {}
    for name, (extra, note) in table.items():
        compose = copy.deepcopy(base)
        compose.update(extra)
        out[name] = {"compose": compose, "note": note}
    return out


def strip(protocol: dict) -> dict:
    for key in ("declaration", "derived_from", "credit"):
        protocol.pop(key, None)
    return protocol


def derive() -> list[str]:
    written = []
    view_template = json.loads((HERE / "protocol-recall-screen-hidden.json").read_text())
    for view in VIEWS:
        p = strip(copy.deepcopy(view_template))
        p["name"] = f"Cadence 0.89 memory on the chain seen {view}: eight recipes, 20 founders"
        p["question"] = ("Do the recall memory with its position term, two heads, a two-event window, the "
                         "learned-code recipe and the episodic vote raise frozen success over the base where "
                         "the stream's history has to tell a stage?")
        p["scope"] = "component reading of the memory options in a world; development founders"
        p["world"] = {**view_template["world"], "view": view}
        p["world"].pop("note", None)
        p["recipes"] = recipes(CHAIN_RECIPES, BASE)
        p["arms"] = copy.deepcopy(VIEW_ARMS)
        p["seeds"] = {"screen": VIEW_SEEDS, "development": VIEW_SEEDS}
        p["training_episodes"] = 120
        name = f"protocol-m089-view-{view}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    for persists, label in ((False, "hidden"), (True, "visible")):
        p = strip(json.loads((HERE / "protocol-p2-route.json").read_text()))
        p["name"] = f"Cadence 0.89 memory on the route cue, cue {label}: eight recipes, 10 founders"
        p["question"] = ("With the cue shown once and then gone, does any memory recipe carry it across the "
                         "neutral events to the first decision, against the cue kept visible?")
        p["scope"] = "component reading of the memory options in a world; development founders"
        p["world"]["cue_persists"] = persists
        p["recipes"] = recipes(CHAIN_RECIPES, BASE)
        p["arms"] = copy.deepcopy(ROUTE_ARMS)
        p["seeds"] = {"development": SEEDS}
        p["withdrawal_episodes"] = 0
        name = f"protocol-m089-route-{label}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    p = strip(json.loads((HERE / "protocol-recall.json").read_text()))
    # the recall world's own base in the 0.89 form: the step sizes come from the founder teaching
    # point (0.5 and 0.05, momentum 0.9; the original set 0.005 for the bias), homeostasis is gone
    # from the library, and the qualified nudged budget equals the free one as the library asks
    base = {"modules": [32], "lateral": 0.0, "episodic": False, "arousal": True,
            "learning_qualified": True, "learning_free_steps": 1024, "learning_nudged_steps": 1024,
            "learning_tolerance": 0.003, "working_memory_decay": 0.0, "working_memory_amplitude": 0.3}
    p["name"] = "Cadence 0.89 memory on the recall world: six recipes, 10 founders"
    p["question"] = "Does the recall memory, with or without its position term, answer the latest written value?"
    p["scope"] = "component reading of the memory options in a world; development founders"
    p["recipes"] = recipes(RECALL_WORLD_RECIPES, base)
    p["seeds"] = {"development": SEEDS}
    (HERE / "protocol-m089-recall.json").write_text(json.dumps(p, indent=1) + "\n")
    written.append("protocol-m089-recall.json")
    p = strip(json.loads((HERE / "protocol-p1-library-defaults.json").read_text()))
    p["name"] = "Cadence 0.89 memory on P1, the observed cold chain: eight recipes, 10 founders"
    p["question"] = "On the fully observed chain, where memory should not matter, does any memory recipe cost success?"
    p["scope"] = "control reading of the memory options; development founders"
    p["recipes"] = recipes(CHAIN_RECIPES, BASE)
    p["seeds"] = {"development": SEEDS}
    (HERE / "protocol-m089-p1.json").write_text(json.dumps(p, indent=1) + "\n")
    written.append("protocol-m089-p1.json")
    return written


READINGS = {
    **{f"view-{v}": (f"protocol-m089-view-{v}.json", CHAIN_RECIPES, VIEW_SEEDS, "defaults") for v in VIEWS},
    "route-hidden": ("protocol-m089-route-hidden.json", CHAIN_RECIPES, SEEDS, "defaults"),
    "route-visible": ("protocol-m089-route-visible.json", CHAIN_RECIPES, SEEDS, "defaults"),
    "recall": ("protocol-m089-recall.json", RECALL_WORLD_RECIPES, SEEDS, "carried"),
    "p1": ("protocol-m089-p1.json", CHAIN_RECIPES, SEEDS, "defaults"),
}
ORDER = ("recall", "route-hidden", "route-visible", "p1", *(f"view-{v}" for v in VIEWS))


def jobs(out: Path) -> None:
    lines = []
    for reading in ORDER:  # the long recall-world lives first
        protocol, table, seeds, _ = READINGS[reading]
        for seed in seeds:
            for recipe in table:
                lines.append(f"{reading} {protocol} {recipe} {seed}")
    (out / "jobs.txt").write_text("\n".join(lines) + "\n")
    print(len(lines), "jobs")


def bootstrap(diffs: np.ndarray, resamples: int = 10000, seed: int = 31012) -> tuple[float, float]:
    if len(diffs) < 2:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    means = diffs[rng.integers(0, len(diffs), size=(resamples, len(diffs)))].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def read_run(path: Path, recipe: str) -> dict | None:
    metrics = path / "metrics.json"
    if not metrics.exists():
        return None
    m = json.loads(metrics.read_text())
    founder = m["recipes"][recipe]["founders"][0]
    out = {"uniform": m["analytic"].get("uniform_random_success")}
    for arm, rec in founder["arms"].items():
        frozen = rec["frozen"]
        s = frozen.get("sampled", {}).get("summary", {})
        g = frozen.get("greedy", {}).get("summary", {})
        counts = rec.get("training", {}).get("counts", {})  # controls have no training
        row = {"sampled": s.get("success_rate", float("nan")), "greedy": g.get("success_rate", float("nan")),
               "first_try": s.get("first_try_accuracy"),
               "labels": counts.get("teaching", {}).get("labels", 0),
               "sweeps": counts.get("teaching", {}).get("sweeps", 0),
               "decisions": counts.get("decisions", 0)}
        withdrawn = rec.get("withdrawal")
        if isinstance(withdrawn, dict) and "frozen" in withdrawn:
            row["withdrawn_sampled"] = withdrawn["frozen"]["sampled"]["summary"]["success_rate"]
        out[arm] = row
    return out


def analyze(out: Path) -> None:
    summary: dict = {}
    lines = ["# Cadence 0.89 memory readings (development founders)", ""]
    for reading in ORDER:
        _, table, seeds, base = READINGS[reading]
        runs = {(r, s): read_run(out / reading / r / f"s{s}", r) for r in table for s in seeds}
        done = {k: v for k, v in runs.items() if v is not None}
        if not done:
            continue
        uniform = next(iter(done.values()))["uniform"]
        arms = [a for a in next(iter(done.values())) if a != "uniform"]
        summary[reading] = {"uniform_random": uniform, "arms": {}}
        chance = f"{uniform:.3f}" if isinstance(uniform, float) else "as in the `random` control rows"
        lines += [f"## {reading}", "", f"Uniform random {chance}. Sampled and greedy frozen success, mean over "
                  f"founders; the difference from `{base}` is founder-paired, bootstrap 95%.", ""]
        lines += ["| Arm | Recipe | Founders | Sampled | Greedy | Sampled - base [95%] | Up/down | Labels | Sweeps |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for arm in arms:
            summary[reading]["arms"][arm] = {}
            for recipe in table:
                rows = {s: done[(recipe, s)][arm] for s in seeds if (recipe, s) in done}
                if not rows:
                    continue
                sampled = np.array([r["sampled"] for r in rows.values()])
                greedy = np.array([r["greedy"] for r in rows.values()])
                paired = [s for s in rows if (base, s) in done]
                diffs = np.array([rows[s]["sampled"] - done[(base, s)][arm]["sampled"] for s in paired])
                lo, hi = bootstrap(diffs) if recipe != base else (float("nan"), float("nan"))
                up, down = int((diffs > 0).sum()), int((diffs < 0).sum())
                entry = {"founders": len(rows), "sampled": float(sampled.mean()), "greedy": float(greedy.mean()),
                         "vs_base": float(diffs.mean()) if len(diffs) else None, "ci": [lo, hi], "up": up, "down": down,
                         "labels": float(np.mean([r["labels"] for r in rows.values()])),
                         "sweeps": float(np.mean([r["sweeps"] for r in rows.values()]))}
                if all("withdrawn_sampled" in r for r in rows.values()):
                    entry["withdrawn_sampled"] = float(np.mean([r["withdrawn_sampled"] for r in rows.values()]))
                ft = [r["first_try"] for r in rows.values() if r.get("first_try")]
                if ft:
                    entry["first_try"] = [float(np.nanmean([f[k] if f[k] is not None else np.nan for f in ft]))
                                          for k in range(len(ft[0]))]
                summary[reading]["arms"][arm][recipe] = entry
                diff = ("" if recipe == base or entry["vs_base"] is None
                        else f"{entry['vs_base']:+.3f} [{lo:+.3f}, {hi:+.3f}]")
                lines.append(f"| {arm} | {recipe} | {len(rows)} | {entry['sampled']:.3f} | {entry['greedy']:.2f} | "
                             f"{diff} | {'' if recipe == base else f'{up}/{down}'} | {entry['labels']:.0f} | "
                             f"{entry['sweeps']:.0f} |")
        lines.append("")
    (out / "m089-summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    (out / "M089_RESULTS.md").write_text("\n".join(lines) + "\n")
    print("readings:", ", ".join(summary))




# -- grid 2: what the first grid's recall world and route cue asked next

RECALL2_RECIPES = {
    "carried": ({}, "the recall world's base"),
    "recall": ({"recall": True}, "the recall memory with its default position term"),
    "recall_nopos": ({"recall": True, "recall_position": 0}, "no position term"),
    "recall_p4": ({"recall": True, "recall_position": 4}, "four exact ages, then one bucket per doubling"),
    "recall_rate03": ({"recall": True, "recall_position_rate": 0.3}, "the position lesson at rate 0.3"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "two heads"),
    "recall_h2_nopos": ({"recall": True, "recall_heads": 2, "recall_position": 0}, "two heads, no position term"),
    "recall_h4": ({"recall": True, "recall_heads": 4}, "four heads"),
    "recall_areward": ({"recall": True, "recall_address_reward": 1.0}, "reward trains the address map"),
    "recall_h2_areward": ({"recall": True, "recall_heads": 2, "recall_address_reward": 1.0},
                          "two heads, reward trains the address maps"),
}
ROUTE2_RECIPES = {
    "defaults": ({}, "the base"),
    "episodic": ({"memory_choice": True}, "the episodic vote"),
    "episodic_recall": ({"memory_choice": True, "recall": True}, "the episodic vote and the recall memory"),
    "episodic_recall_nopos": ({"memory_choice": True, "recall": True, "recall_position": 0},
                              "the episodic vote and the recall memory without the position term"),
    "episodic_recall_h2": ({"memory_choice": True, "recall": True, "recall_heads": 2},
                           "the episodic vote and two recall heads"),
    "episodic_recall_areward": ({"memory_choice": True, "recall": True, "recall_address_reward": 1.0},
                                "the episodic vote and the recall memory whose address reward trains"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "two recall heads"),
    "recall_h2_areward": ({"recall": True, "recall_heads": 2, "recall_address_reward": 1.0},
                          "two recall heads, reward trains the address maps"),
}
ROUTE2_ARMS = {
    "guide_step": {"adapter": "step", "caregiver": "guide"},
    "grade_step": {"adapter": "step", "caregiver": "grade"},
    "natural_live": {"adapter": "live", "caregiver": "none"},
    "guide_step_1920": {"adapter": "step", "caregiver": "guide", "training_episodes": 1920},
    "natural_live_1920": {"adapter": "live", "caregiver": "none", "training_episodes": 1920},
}
SEEDS2 = list(range(1011, 1031))


def derive2() -> list[str]:
    written = []
    p = json.loads((HERE / "protocol-m089-recall.json").read_text())
    base = p["recipes"]["carried"]["compose"]
    p["name"] = "Cadence 0.89 memory on the recall world, second grid: ten recipes, 20 new founders"
    p["recipes"] = recipes(RECALL2_RECIPES, base)
    p["seeds"] = {"development": SEEDS2}
    (HERE / "protocol-m089b-recall.json").write_text(json.dumps(p, indent=1) + "\n")
    written.append("protocol-m089b-recall.json")
    for label in ("hidden", "visible"):
        p = json.loads((HERE / f"protocol-m089-route-{label}.json").read_text())
        p["name"] = f"Cadence 0.89 memory on the route cue, cue {label}, second grid: 20 new founders"
        p["recipes"] = recipes(ROUTE2_RECIPES, BASE)
        p["arms"] = copy.deepcopy(ROUTE2_ARMS)
        p["seeds"] = {"development": SEEDS2}
        name = f"protocol-m089b-route-{label}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS2 = {
    "recall2": ("protocol-m089b-recall.json", RECALL2_RECIPES, SEEDS2, "carried"),
    "route2-hidden": ("protocol-m089b-route-hidden.json", ROUTE2_RECIPES, SEEDS2, "defaults"),
    "route2-visible": ("protocol-m089b-route-visible.json", ROUTE2_RECIPES, SEEDS2, "defaults"),
}


def use_grid(grid: str) -> None:
    """Point the jobs and the analysis at one grid's readings."""
    global READINGS, ORDER
    if grid == "2":
        READINGS = READINGS2
        ORDER = tuple(READINGS2)
    if grid == "3":
        READINGS = READINGS3
        ORDER = tuple(READINGS3)
    if grid == "4":
        READINGS = READINGS4
        ORDER = ("route4-hidden", "view4-hidden")
    if grid == "5":
        READINGS = READINGS5
        ORDER = tuple(READINGS5)
    if grid == "6":
        READINGS = READINGS6
        ORDER = tuple(reversed(tuple(READINGS6)))  # the longest delays first
    if grid == "7":
        READINGS = READINGS7
        ORDER = tuple(READINGS7)
    if grid == "8":
        READINGS = READINGS8
        ORDER = ("route8-delay16", "route8-delay8")
    if grid == "9":
        READINGS = READINGS9
        ORDER = ("route9-delay16", "route9-delay8")
    if grid == "10":
        READINGS = READINGS10
        ORDER = tuple(READINGS10)
    if grid == "11":
        READINGS = READINGS11
        ORDER = tuple(READINGS11)
    if grid == "12":
        READINGS = READINGS12
        ORDER = ("route12-16-hidden", "route12-16-visible", "route12-8-hidden", "route12-8-visible")
    if grid == "13":
        READINGS = READINGS13
        ORDER = tuple(READINGS13)
    if grid == "14":
        READINGS = READINGS14
        ORDER = tuple(READINGS14)
    if grid == "15":
        READINGS = READINGS15
        ORDER = tuple(READINGS15)
    if grid == "16":
        READINGS = READINGS16
        ORDER = tuple(READINGS16)
    if grid == "17":
        READINGS = READINGS17
        ORDER = tuple(READINGS17)


# -- founder-paired contrasts between recipes: what one mechanism adds to another

PAIRS = {
    "chain": [("recall", "recall_nopos"), ("recall_h2", "recall"), ("recall_w2", "recall"),
              ("attention", "recall"), ("episodic_recall", "episodic"), ("episodic_recall", "recall")],
    "recall": [("recall", "recall_nopos"), ("recall_h2", "recall"), ("attention", "recall"),
               ("recall", "retained")],
    "recall2": [("recall", "recall_nopos"), ("recall_h2", "recall_h2_nopos"), ("recall_p4", "recall"),
                ("recall_rate03", "recall"), ("recall_h2", "recall"), ("recall_h4", "recall_h2"),
                ("recall_areward", "recall"), ("recall_h2_areward", "recall_h2")],
    "route2": [("episodic_recall", "episodic"), ("episodic_recall", "episodic_recall_nopos"),
               ("episodic_recall_h2", "episodic_recall"), ("episodic_recall_areward", "episodic_recall"),
               ("recall_h2_areward", "recall_h2")],
}


def pair_family(reading: str) -> str:
    if reading == "recall":
        return "recall"
    if reading == "recall2":
        return "recall2"
    if reading.startswith("route2"):
        return "route2"
    if reading.startswith("view3"):
        return "view3"
    if reading.startswith("view4") or reading.startswith("route4"):
        return "grid4"
    if reading == "recall-order":
        return "order"
    if reading.startswith("route6"):
        return "delay"
    if reading == "recall-order-code":
        return "code"
    if reading.startswith("route8"):
        return "long"
    if reading.startswith("route9"):
        return "vote"
    if reading.startswith("route12"):
        return "longlesson"
    if "13-" in reading:
        return "rep"
    if reading.startswith("route14"):
        return "alone"
    if reading.startswith("recall15"):
        return "gap"
    if reading == "recall16-gap96":
        return "gap96"
    if reading == "view17-hidden":
        return "hidden17"
    if reading.startswith("recall16"):
        return "gap"
    if reading.endswith("10-plain") or reading.endswith("10-order") or "10-" in reading:
        return "r0"
    if reading.startswith("view11"):
        return "chain"
    if reading.startswith("route12"):
        return "longlesson"
    return "chain"


def contrasts(out: Path) -> None:
    result: dict = {}
    lines = ["# Founder-paired contrasts between recipes", "",
             "Sampled frozen success, recipe A minus recipe B on the same founders and arm; bootstrap 95%.", ""]
    for reading in ORDER:
        _, table, seeds, _ = READINGS[reading]
        runs = {(r, s): read_run(out / reading / r / f"s{s}", r) for r in table for s in seeds}
        done = {k: v for k, v in runs.items() if v is not None}
        if not done:
            continue
        arms = [a for a in next(iter(done.values())) if a not in ("uniform", "random", "oracle", "searcher", "founder")]
        lines += [f"## {reading}", "", "| Arm | A - B | Founders | Mean [95%] | Up/down |", "| --- | --- | --- | --- | --- |"]
        result[reading] = {}
        for a, b in PAIRS[pair_family(reading)]:
            if a not in table or b not in table:
                continue
            for arm in arms:
                paired = [s for s in seeds if (a, s) in done and (b, s) in done]
                if len(paired) < 2:
                    continue
                diffs = np.array([done[(a, s)][arm]["sampled"] - done[(b, s)][arm]["sampled"] for s in paired])
                lo, hi = bootstrap(diffs)
                key = f"{a} - {b}"
                result[reading].setdefault(key, {})[arm] = {"founders": len(paired), "mean": float(diffs.mean()),
                                                            "ci": [lo, hi], "up": int((diffs > 0).sum()),
                                                            "down": int((diffs < 0).sum())}
                lines.append(f"| {arm} | {key} | {len(paired)} | {diffs.mean():+.3f} [{lo:+.3f}, {hi:+.3f}] | "
                             f"{int((diffs > 0).sum())}/{int((diffs < 0).sum())} |")
        lines.append("")
    (out / "m089-contrasts.json").write_text(json.dumps(result, indent=1) + "\n")
    (out / "M089_CONTRASTS.md").write_text("\n".join(lines) + "\n")
    print("contrast readings:", ", ".join(result))



# -- grid 3: the position term on 40 more founders, a quieter read, and the best combination

VIEW3_RECIPES = {
    "recall": ({"recall": True}, "the recall memory with its default position term"),
    "recall_nopos": ({"recall": True, "recall_position": 0}, "no position term"),
    "recall_quiet": ({"recall": True, "recall_amplitude": 1.0}, "the read held at amplitude 1 in place of 3"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "two heads"),
    "episodic": ({"memory_choice": True}, "the episodic vote"),
    "episodic_recall": ({"memory_choice": True, "recall": True}, "the vote and the recall memory"),
    "episodic_recall_nopos": ({"memory_choice": True, "recall": True, "recall_position": 0},
                              "the vote and the recall memory without the position term"),
    "episodic_recall_h2": ({"memory_choice": True, "recall": True, "recall_heads": 2},
                           "the vote and two recall heads"),
}
VIEW3_ARMS = {
    "corrective_step_120": {"adapter": "step", "caregiver": "correct", "training_episodes": 120},
    "corrective_step_480": {"adapter": "step", "caregiver": "correct", "training_episodes": 480},
    "natural_live_480": {"adapter": "live", "caregiver": "none", "training_episodes": 480},
}
VIEW3_SEEDS = list(range(202021, 202061))
VIEWS3 = ("hidden", "invisible", "visible")


def derive3() -> list[str]:
    written = []
    for view in VIEWS3:
        p = json.loads((HERE / f"protocol-m089-view-{view}.json").read_text())
        p["name"] = f"Cadence 0.89 memory on the chain seen {view}, third grid: 40 new founders"
        p["recipes"] = recipes(VIEW3_RECIPES, BASE)
        p["arms"] = copy.deepcopy(VIEW3_ARMS)
        p["seeds"] = {"screen": VIEW3_SEEDS, "development": VIEW3_SEEDS}
        name = f"protocol-m089c-view-{view}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS3 = {f"view3-{v}": (f"protocol-m089c-view-{v}.json", VIEW3_RECIPES, VIEW3_SEEDS, "recall_nopos")
             for v in VIEWS3}
PAIRS["view3"] = [("recall", "recall_nopos"), ("episodic_recall", "episodic_recall_nopos"),
                  ("episodic_recall", "episodic"), ("episodic_recall_h2", "episodic_recall"),
                  ("recall_quiet", "recall"), ("recall_h2", "recall")]



# -- grid 4: longer lives, a wider brain and no recency charge, where the cue is still lost

BIG = {"modules": [96, 48], "arousal": True}
GRID4_RECIPES = {
    "defaults_big": ({"modules": [96, 48]}, "the base at twice the width"),
    "episodic": ({"memory_choice": True}, "the episodic vote"),
    "episodic_big": ({"modules": [96, 48], "memory_choice": True}, "the vote at twice the width"),
    "recall": ({"recall": True}, "the recall memory"),
    "recall_big": ({"modules": [96, 48], "recall": True}, "the recall memory at twice the width"),
    "episodic_recall": ({"memory_choice": True, "recall": True}, "the vote and the recall memory"),
    "episodic_recall_r0": ({"memory_choice": True, "recall": True, "recall_recency": 0.0},
                           "the vote and the recall memory without the recency charge"),
    "episodic_recall_big": ({"modules": [96, 48], "memory_choice": True, "recall": True},
                            "the vote and the recall memory at twice the width"),
    "episodic_recall_h2_big": ({"modules": [96, 48], "memory_choice": True, "recall": True, "recall_heads": 2},
                               "the vote and two recall heads at twice the width"),
}
VIEW4_ARMS = {
    "corrective_step_480": {"adapter": "step", "caregiver": "correct", "training_episodes": 480},
    "corrective_step_1920": {"adapter": "step", "caregiver": "correct", "training_episodes": 1920},
    "natural_live_1920": {"adapter": "live", "caregiver": "none", "training_episodes": 1920},
}
ROUTE4_ARMS = {
    "guide_step_1920": {"adapter": "step", "caregiver": "guide", "training_episodes": 1920},
    "natural_live_1920": {"adapter": "live", "caregiver": "none", "training_episodes": 1920},
}
SEEDS4 = list(range(1001, 1021))


def derive4() -> list[str]:
    written = []
    p = json.loads((HERE / "protocol-m089-view-hidden.json").read_text())
    p["name"] = "Cadence 0.89 memory on the hidden view, fourth grid: longer lives, a wider brain"
    p["recipes"] = recipes(GRID4_RECIPES, BASE)
    p["arms"] = copy.deepcopy(VIEW4_ARMS)
    (HERE / "protocol-m089d-view-hidden.json").write_text(json.dumps(p, indent=1) + "\n")
    written.append("protocol-m089d-view-hidden.json")
    p = json.loads((HERE / "protocol-m089-route-hidden.json").read_text())
    p["name"] = "Cadence 0.89 memory on the hidden route cue, fourth grid: longer lives, a wider brain"
    p["recipes"] = recipes(GRID4_RECIPES, BASE)
    p["arms"] = copy.deepcopy(ROUTE4_ARMS)
    p["seeds"] = {"development": SEEDS4}
    (HERE / "protocol-m089d-route-hidden.json").write_text(json.dumps(p, indent=1) + "\n")
    written.append("protocol-m089d-route-hidden.json")
    return written


READINGS4 = {
    "view4-hidden": ("protocol-m089d-view-hidden.json", GRID4_RECIPES, VIEW_SEEDS, "episodic"),
    "route4-hidden": ("protocol-m089d-route-hidden.json", GRID4_RECIPES, SEEDS4, "episodic"),
}
PAIRS["grid4"] = [("episodic_big", "episodic"), ("episodic_recall_big", "episodic_recall"),
                  ("episodic_recall", "episodic"), ("episodic_recall_r0", "episodic_recall"),
                  ("recall_big", "recall"), ("episodic_recall_h2_big", "episodic_recall_big"),
                  ("defaults_big", "episodic_big")]



# -- grid 5: the ordered recall world (first or latest written value), and per-condition readings

ORDER_RECIPES = {
    "carried": ({}, "the recall world's base"),
    "retained": ({"working_memory_decay": 0.8}, "a retained working trace"),
    "recall": ({"recall": True}, "the recall memory with its default position term"),
    "recall_nopos": ({"recall": True, "recall_position": 0}, "no position term"),
    "recall_r0": ({"recall": True, "recall_recency": 0.0}, "no recency charge"),
    "recall_nopos_r0": ({"recall": True, "recall_position": 0, "recall_recency": 0.0},
                        "no position term and no recency charge"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "two heads"),
    "recall_h2_nopos": ({"recall": True, "recall_heads": 2, "recall_position": 0}, "two heads, no position"),
    "attention": ({"attention": True, "learned_code": 8}, "the learned-code contextual recipe"),
}
SEEDS5 = list(range(1001, 1021))


def derive5() -> list[str]:
    p = json.loads((HERE / "protocol-m089-recall.json").read_text())
    p["name"] = "Cadence 0.89 memory on the ordered recall world: the first or the latest written value"
    p["question"] = ("Two values are written, then asked: the first through a query marker of its own, or "
                     "the latest. Does the position term let a lesson teach the read to look back to the "
                     "older write?")
    p["world"] = {**p["world"], "ask": "order"}
    p["recipes"] = recipes(ORDER_RECIPES, p["recipes"]["carried"]["compose"])
    p["seeds"] = {"development": SEEDS5}
    (HERE / "protocol-m089e-recall-order.json").write_text(json.dumps(p, indent=1) + "\n")
    return ["protocol-m089e-recall-order.json"]


READINGS5 = {"recall-order": ("protocol-m089e-recall-order.json", ORDER_RECIPES, SEEDS5, "carried")}
PAIRS["order"] = [("recall", "recall_nopos"), ("recall_r0", "recall_nopos_r0"), ("recall_h2", "recall_h2_nopos"),
                  ("recall_r0", "recall"), ("attention", "recall"), ("recall", "retained")]


def conditions_of(run: Path) -> dict:
    """Sampled success per arm and condition of one recall run, from its episode table."""
    import csv  # noqa: PLC0415
    out: dict = {}
    for table in run.glob("*/founder-*/episodes.csv"):
        with table.open() as f:
            for row in csv.DictReader(f):
                if row["phase"] not in ("trained", "withdrawn") or row["mode"] != "sampled":
                    continue
                condition = json.loads(row["route"])["condition"]
                arm = row["arm"] if row["phase"] == "trained" else row["arm"] + "+alone"
                cell = out.setdefault(arm, {}).setdefault(condition, [0, 0])
                cell[0] += row["success"] == "True"
                cell[1] += 1
    return {arm: {c: s / n for c, (s, n) in conds.items()} for arm, conds in out.items()}


def by_condition(out: Path) -> None:
    """Per recall reading, recipe, arm and condition: the mean over founders, and the position
    term's founder-paired effect per condition."""
    result: dict = {}
    lines = ["# Recall readings per condition", ""]
    for reading in ORDER:
        if not reading.startswith("recall"):
            continue
        _, table, seeds, _ = READINGS[reading]
        runs = {(r, s): conditions_of(out / reading / r / f"s{s}") for r in table for s in seeds
                if (out / reading / r / f"s{s}" / "metrics.json").exists()}
        if not runs:
            continue
        result[reading] = {}
        lines += [f"## {reading}", ""]
        arms = sorted({a for v in runs.values() for a in v if a not in ("random", "oracle")})
        conds = sorted({c for v in runs.values() for a in v.values() for c in a})
        lines += ["| Arm | Recipe | " + " | ".join(conds) + " |", "| --- | --- |" + " --- |" * len(conds)]
        for arm in arms:
            for recipe in table:
                cells = [runs[(recipe, s)].get(arm, {}) for s in seeds if (recipe, s) in runs]
                if not cells:
                    continue
                means = {c: float(np.mean([x[c] for x in cells if c in x])) for c in conds
                         if any(c in x for x in cells)}
                result[reading].setdefault(arm, {})[recipe] = means
                lines.append(f"| {arm} | {recipe} | " + " | ".join(f"{means.get(c, float('nan')):.2f}" for c in conds) + " |")
        lines.append("")
    (out / "m089-conditions.json").write_text(json.dumps(result, indent=1) + "\n")
    (out / "M089_CONDITIONS.md").write_text("\n".join(lines) + "\n")
    print("condition readings:", ", ".join(result))



# -- grid 6: the vanished route cue at longer delays (2, 4 and 8 neutral events)

DELAY_RECIPES = {
    "episodic": ({"memory_choice": True}, "the episodic vote"),
    "episodic_recall": ({"memory_choice": True, "recall": True}, "the vote and the recall memory"),
    "episodic_recall_nopos": ({"memory_choice": True, "recall": True, "recall_position": 0},
                              "the vote and the recall memory without the position term"),
    "episodic_recall_h2": ({"memory_choice": True, "recall": True, "recall_heads": 2},
                           "the vote and two recall heads"),
    "recall": ({"recall": True}, "the recall memory"),
    "recall_nopos": ({"recall": True, "recall_position": 0}, "the recall memory without the position term"),
}
DELAY_ARMS = {
    "guide_step_1920": {"adapter": "step", "caregiver": "guide", "training_episodes": 1920},
    "natural_live_1920": {"adapter": "live", "caregiver": "none", "training_episodes": 1920},
}
DELAYS = (2, 4, 8)


def derive6() -> list[str]:
    written = []
    for delay in DELAYS:
        p = json.loads((HERE / "protocol-m089-route-hidden.json").read_text())
        p["name"] = f"Cadence 0.89 memory on the vanished route cue across {delay} neutral events"
        p["world"] = {**p["world"], "neutral": delay}
        p["recipes"] = recipes(DELAY_RECIPES, BASE)
        p["arms"] = copy.deepcopy(DELAY_ARMS)
        p["seeds"] = {"development": SEEDS4}
        name = f"protocol-m089f-route-delay{delay}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS6 = {f"route6-delay{d}": (f"protocol-m089f-route-delay{d}.json", DELAY_RECIPES, SEEDS4, "episodic")
             for d in DELAYS}
PAIRS["delay"] = [("episodic_recall", "episodic"), ("episodic_recall", "episodic_recall_nopos"),
                  ("episodic_recall_h2", "episodic_recall"), ("recall", "recall_nopos")]



# -- grid 7: the ordered recall world with learned codes, reward-trained addresses, and a life alone

CODE_RECIPES = {
    "recall": ({"recall": True}, "the recall memory on the observation"),
    "recall_nopos": ({"recall": True, "recall_position": 0}, "no position term"),
    "code8": ({"recall": True, "learned_code": 8}, "the recall memory on a learned code of 8 units"),
    "code16": ({"recall": True, "learned_code": 16}, "the recall memory on a learned code of 16 units"),
    "att8": ({"attention": True, "learned_code": 8}, "the contextual recipe, 8 units"),
    "att16": ({"attention": True, "learned_code": 16}, "the contextual recipe, 16 units"),
    "att16_addr": ({"attention": True, "learned_code": 16, "recall_address": 0.01},
                   "the contextual recipe, 16 units, with the address lesson on"),
    "recall_areward": ({"recall": True, "recall_address_reward": 1.0}, "reward trains the address map"),
    "recall_h2_areward": ({"recall": True, "recall_heads": 2, "recall_address_reward": 1.0},
                          "two heads, reward trains the address maps"),
}
CODE_ARMS = {
    "teach_step": {"adapter": "step", "caregiver": "guide", "withdrawal_adapter": "live"},
    "reward_live": {"adapter": "live", "caregiver": "none"},
}


def derive7() -> list[str]:
    p = json.loads((HERE / "protocol-m089e-recall-order.json").read_text())
    p["name"] = "Cadence 0.89 memory on the ordered recall world: learned codes, reward-trained addresses, a life alone"
    p["recipes"] = recipes(CODE_RECIPES, json.loads((HERE / "protocol-m089e-recall-order.json").read_text())["recipes"]["carried"]["compose"])
    p["arms"] = copy.deepcopy(CODE_ARMS)
    p["withdrawal_episodes"] = 512
    (HERE / "protocol-m089g-recall-order-code.json").write_text(json.dumps(p, indent=1) + "\n")
    return ["protocol-m089g-recall-order-code.json"]


READINGS7 = {"recall-order-code": ("protocol-m089g-recall-order-code.json", CODE_RECIPES, SEEDS5, "recall")}
PAIRS["code"] = [("recall", "recall_nopos"), ("code8", "recall"), ("code16", "recall"), ("att16", "att8"),
                 ("att16_addr", "att16"), ("recall_areward", "recall"), ("recall_h2_areward", "recall_areward")]



# -- grid 8: the recall memory alone at long delays (8 and 16 neutral events), recency on and off

LONG_RECIPES = {
    "recall": ({"recall": True}, "the recall memory"),
    "recall_nopos": ({"recall": True, "recall_position": 0}, "no position term"),
    "recall_r0": ({"recall": True, "recall_recency": 0.0}, "no recency charge"),
    "recall_nopos_r0": ({"recall": True, "recall_position": 0, "recall_recency": 0.0},
                        "no position term, no recency charge"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "two heads"),
    "episodic": ({"memory_choice": True}, "the episodic vote"),
    "episodic_recall_r0": ({"memory_choice": True, "recall": True, "recall_recency": 0.0},
                           "the vote and the recall memory without the recency charge"),
}
LONG_DELAYS = (8, 16)


def derive8() -> list[str]:
    written = []
    for delay in LONG_DELAYS:
        p = json.loads((HERE / "protocol-m089-route-hidden.json").read_text())
        p["name"] = f"Cadence 0.89 recall memory alone on the vanished route cue across {delay} neutral events"
        p["world"] = {**p["world"], "neutral": delay}
        p["recipes"] = recipes(LONG_RECIPES, BASE)
        p["arms"] = copy.deepcopy(DELAY_ARMS)
        p["seeds"] = {"development": SEEDS4}
        name = f"protocol-m089h-route-long{delay}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS8 = {f"route8-delay{d}": (f"protocol-m089h-route-long{d}.json", LONG_RECIPES, SEEDS4, "recall_nopos")
             for d in LONG_DELAYS}
PAIRS["long"] = [("recall", "recall_nopos"), ("recall_r0", "recall_nopos_r0"), ("recall_r0", "recall"),
                 ("recall_h2", "recall"), ("recall", "episodic"), ("episodic_recall_r0", "episodic")]



# -- grid 9: the episodic vote's context horizon and weight against the read, at long delays

VOTE_RECIPES = {
    "episodic": ({"memory_choice": True}, "the episodic vote, context 0.5"),
    "episodic_ctx08": ({"memory_choice": True, "memory_context": 0.8}, "the vote, context 0.8"),
    "episodic_ctx09": ({"memory_choice": True, "memory_context": 0.9}, "the vote, context 0.9"),
    "episodic_recall_ctx09": ({"memory_choice": True, "memory_context": 0.9, "recall": True},
                              "the vote at context 0.9 and the recall memory"),
    "episodic_amp05": ({"memory_choice": True, "memory_amplitude": 0.5}, "the vote at half weight"),
    "episodic_recall_amp05": ({"memory_choice": True, "memory_amplitude": 0.5, "recall": True},
                              "the vote at half weight and the recall memory"),
    "recall": ({"recall": True}, "the recall memory alone"),
}


def derive9() -> list[str]:
    written = []
    for delay in LONG_DELAYS:
        p = json.loads((HERE / f"protocol-m089h-route-long{delay}.json").read_text())
        p["name"] = f"Cadence 0.89 episodic vote and recall on the vanished route cue across {delay} neutral events"
        p["recipes"] = recipes(VOTE_RECIPES, BASE)
        name = f"protocol-m089i-route-vote{delay}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS9 = {f"route9-delay{d}": (f"protocol-m089i-route-vote{d}.json", VOTE_RECIPES, SEEDS4, "episodic")
             for d in LONG_DELAYS}
PAIRS["vote"] = [("episodic_ctx08", "episodic"), ("episodic_ctx09", "episodic"),
                 ("episodic_recall_ctx09", "episodic_ctx09"), ("episodic_amp05", "episodic"),
                 ("episodic_recall_amp05", "episodic_amp05"), ("recall", "episodic")]



# -- grid 10: recency 0 as the founder candidate with the position term, on new founders across worlds

R0_RECIPES = {
    "recall": ({"recall": True}, "the recall memory at the founder recency 0.25"),
    "recall_r0": ({"recall": True, "recall_recency": 0.0}, "the recall memory at recency 0"),
    "episodic_recall": ({"memory_choice": True, "recall": True}, "the vote and the recall memory, recency 0.25"),
    "episodic_recall_r0": ({"memory_choice": True, "recall": True, "recall_recency": 0.0},
                           "the vote and the recall memory, recency 0"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "two heads, recency 0.25"),
    "recall_h2_r0": ({"recall": True, "recall_heads": 2, "recall_recency": 0.0}, "two heads, recency 0"),
}
R0_RECALL_RECIPES = {
    "recall": ({"recall": True}, "the recall memory at the founder recency 0.25"),
    "recall_r0": ({"recall": True, "recall_recency": 0.0}, "the recall memory at recency 0"),
    "recall_h2": ({"recall": True, "recall_heads": 2}, "two heads, recency 0.25"),
    "recall_h2_r0": ({"recall": True, "recall_heads": 2, "recall_recency": 0.0}, "two heads, recency 0"),
}
SEEDS10 = list(range(1021, 1041))


def derive10() -> list[str]:
    written = []
    for view in ("hidden", "visible"):
        p = json.loads((HERE / f"protocol-m089c-view-{view}.json").read_text())
        p["name"] = f"Cadence 0.89 recency 0 with the position term on the chain seen {view}: 40 founders"
        p["recipes"] = recipes(R0_RECIPES, BASE)
        name = f"protocol-m089j-view-{view}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    for delay in (2, 16):
        p = json.loads((HERE / f"protocol-m089f-route-delay{min(delay, 8)}.json").read_text())
        p["name"] = f"Cadence 0.89 recency 0 with the position term on the route cue across {delay} neutral events"
        p["world"] = {**p["world"], "neutral": delay}
        p["recipes"] = recipes(R0_RECIPES, BASE)
        p["seeds"] = {"development": SEEDS10}
        name = f"protocol-m089j-route-delay{delay}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    for label, source in (("plain", "protocol-m089-recall.json"), ("order", "protocol-m089e-recall-order.json")):
        p = json.loads((HERE / source).read_text())
        p["name"] = f"Cadence 0.89 recency 0 with the position term on the {label} recall world"
        p["recipes"] = recipes(R0_RECALL_RECIPES, p["recipes"]["carried"]["compose"])
        p["seeds"] = {"development": SEEDS10}
        name = f"protocol-m089j-recall-{label}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS10 = {
    "recall10-plain": ("protocol-m089j-recall-plain.json", R0_RECALL_RECIPES, SEEDS10, "recall"),
    "recall10-order": ("protocol-m089j-recall-order.json", R0_RECALL_RECIPES, SEEDS10, "recall"),
    "route10-delay16": ("protocol-m089j-route-delay16.json", R0_RECIPES, SEEDS10, "recall"),
    "route10-delay2": ("protocol-m089j-route-delay2.json", R0_RECIPES, SEEDS10, "recall"),
    "view10-hidden": ("protocol-m089j-view-hidden.json", R0_RECIPES, VIEW3_SEEDS, "recall"),
    "view10-visible": ("protocol-m089j-view-visible.json", R0_RECIPES, VIEW3_SEEDS, "recall"),
}
PAIRS["r0"] = [("recall_r0", "recall"), ("episodic_recall_r0", "episodic_recall"), ("recall_h2_r0", "recall_h2")]



# -- grid 11: the chain views with the brain's last executed action in the observation

EFF_RECIPES = {k: CHAIN_RECIPES[k] for k in ("defaults", "recall", "recall_nopos", "episodic", "episodic_recall")}
EFF_VIEWS = ("hidden", "invisible", "consecutive")


def derive11() -> list[str]:
    written = []
    for view in EFF_VIEWS:
        p = json.loads((HERE / f"protocol-m089-view-{view}.json").read_text())
        p["name"] = f"Cadence 0.89 memory on the chain seen {view}, the last executed action shown"
        p["world"] = {**p["world"], "efference": True}
        p["recipes"] = recipes(EFF_RECIPES, BASE)
        name = f"protocol-m089k-view-{view}-efference.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS11 = {f"view11-{v}": (f"protocol-m089k-view-{v}-efference.json", EFF_RECIPES, VIEW_SEEDS, "defaults")
              for v in EFF_VIEWS}



# -- grid 12: the long-delay route with longer lessons (3840 guided episodes)

LONGLESSON_RECIPES = {
    "episodic": ({"memory_choice": True}, "the episodic vote"),
    "recall_r0": ({"recall": True, "recall_recency": 0.0}, "the recall memory at recency 0"),
    "recall_h2_r0": ({"recall": True, "recall_heads": 2, "recall_recency": 0.0}, "two heads at recency 0"),
    "episodic_recall_r0": ({"memory_choice": True, "recall": True, "recall_recency": 0.0},
                           "the vote and the recall memory at recency 0"),
}
LONGLESSON_ARMS = {"guide_step_3840": {"adapter": "step", "caregiver": "guide", "training_episodes": 3840}}


def derive12() -> list[str]:
    written = []
    for delay in LONG_DELAYS:
        for persists, label in ((False, "hidden"), (True, "visible")):
            p = json.loads((HERE / f"protocol-m089h-route-long{delay}.json").read_text())
            p["name"] = f"Cadence 0.89 memory on the route cue, cue {label}, {delay} neutral events, 3840 guided episodes"
            p["world"] = {**p["world"], "cue_persists": persists}
            p["recipes"] = recipes(LONGLESSON_RECIPES, BASE)
            p["arms"] = copy.deepcopy(LONGLESSON_ARMS)
            name = f"protocol-m089l-route{delay}-{label}.json"
            (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
            written.append(name)
    return written


READINGS12 = {f"route12-{d}-{v}": (f"protocol-m089l-route{d}-{v}.json", LONGLESSON_RECIPES, SEEDS4, "episodic")
              for d in LONG_DELAYS for v in ("hidden", "visible")}
PAIRS["longlesson"] = [("recall_r0", "episodic"), ("recall_h2_r0", "recall_r0"), ("episodic_recall_r0", "episodic")]



# -- grid 13: the headline effects again on fresh founders

SEEDS13 = list(range(1041, 1061))
VIEW13_SEEDS = list(range(202061, 202081))
REP_ORDER = {k: ORDER_RECIPES[k] for k in ("recall", "recall_nopos", "recall_h2", "recall_h2_nopos")}
REP_VIEW = {k: EFF_RECIPES[k] for k in ("recall", "episodic", "episodic_recall")}
REP_ROUTE = {k: R0_RECIPES[k] for k in ("recall", "recall_r0", "recall_h2", "recall_h2_r0")}
REP_VIEW_ARMS = {k: VIEW_ARMS[k] for k in ("corrective_step_120", "natural_live_480")}


def derive13() -> list[str]:
    written = []
    p = json.loads((HERE / "protocol-m089e-recall-order.json").read_text())
    p["name"] = "Cadence 0.89 replication: the position term on the ordered recall world, fresh founders"
    p["recipes"] = recipes(REP_ORDER, p["recipes"]["carried"]["compose"])
    p["seeds"] = {"development": SEEDS13}
    (HERE / "protocol-m089m-recall-order.json").write_text(json.dumps(p, indent=1) + "\n")
    written.append("protocol-m089m-recall-order.json")
    for view in ("consecutive", "invisible"):
        for eff in (False, True):
            p = json.loads((HERE / f"protocol-m089-view-{view}.json").read_text())
            p["name"] = f"Cadence 0.89 replication: the chain seen {view}, the last action {'shown' if eff else 'hidden'}"
            p["world"] = {**p["world"], "efference": eff}
            p["recipes"] = recipes(REP_VIEW, BASE)
            p["arms"] = copy.deepcopy(REP_VIEW_ARMS)
            p["seeds"] = {"screen": VIEW13_SEEDS, "development": VIEW13_SEEDS}
            name = f"protocol-m089m-view-{view}{'-efference' if eff else ''}.json"
            (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
            written.append(name)
    p = json.loads((HERE / "protocol-m089j-route-delay16.json").read_text())
    p["name"] = "Cadence 0.89 replication: the route cue across 16 neutral events, recency 0, fresh founders"
    p["recipes"] = recipes(REP_ROUTE, BASE)
    p["arms"] = {"guide_step_1920": copy.deepcopy(DELAY_ARMS["guide_step_1920"])}
    p["seeds"] = {"development": SEEDS13}
    (HERE / "protocol-m089m-route-delay16.json").write_text(json.dumps(p, indent=1) + "\n")
    written.append("protocol-m089m-route-delay16.json")
    return written


READINGS13 = {
    "route13-delay16": ("protocol-m089m-route-delay16.json", REP_ROUTE, SEEDS13, "recall"),
    "recall13-order": ("protocol-m089m-recall-order.json", REP_ORDER, SEEDS13, "recall_nopos"),
    "view13-consecutive": ("protocol-m089m-view-consecutive.json", REP_VIEW, VIEW13_SEEDS, "recall"),
    "view13-consecutive-efference": ("protocol-m089m-view-consecutive-efference.json", REP_VIEW, VIEW13_SEEDS, "recall"),
    "view13-invisible": ("protocol-m089m-view-invisible.json", REP_VIEW, VIEW13_SEEDS, "recall"),
    "view13-invisible-efference": ("protocol-m089m-view-invisible-efference.json", REP_VIEW, VIEW13_SEEDS, "recall"),
}
PAIRS["rep"] = [("recall", "recall_nopos"), ("recall_h2", "recall_h2_nopos"), ("recall_r0", "recall"),
                ("recall_h2_r0", "recall_h2"), ("episodic_recall", "episodic"), ("episodic", "recall")]



# -- grid 14: guided route brains that then live alone, fresh founders

ALONE_RECIPES = {
    "episodic": ({"memory_choice": True}, "the episodic vote"),
    "episodic_recall": ({"memory_choice": True, "recall": True}, "the vote and the recall memory"),
    "episodic_recall_r0": ({"memory_choice": True, "recall": True, "recall_recency": 0.0},
                           "the vote and the recall memory at recency 0"),
    "episodic_recall_h2": ({"memory_choice": True, "recall": True, "recall_heads": 2},
                           "the vote and two recall heads"),
    "recall_r0": ({"recall": True, "recall_recency": 0.0}, "the recall memory at recency 0"),
    "recall_h2_r0": ({"recall": True, "recall_heads": 2, "recall_recency": 0.0}, "two heads at recency 0"),
}
ALONE_ARMS = {
    "guide_step_1920": {"adapter": "step", "caregiver": "guide", "training_episodes": 1920,
                        "withdrawal_adapter": "live"},
    "natural_live_1920": {"adapter": "live", "caregiver": "none", "training_episodes": 1920},
}


def derive14() -> list[str]:
    written = []
    for delay in (2, 16):
        p = json.loads((HERE / f"protocol-m089j-route-delay{delay}.json").read_text())
        p["name"] = f"Cadence 0.89 memory on the route cue across {delay} neutral events: guided, then 1920 alone"
        p["recipes"] = recipes(ALONE_RECIPES, BASE)
        p["arms"] = copy.deepcopy(ALONE_ARMS)
        p["seeds"] = {"development": SEEDS13}
        p["withdrawal_episodes"] = 1920
        name = f"protocol-m089n-route-delay{delay}-alone.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS14 = {f"route14-delay{d}": (f"protocol-m089n-route-delay{d}-alone.json", ALONE_RECIPES, SEEDS13, "episodic")
              for d in (16, 2)}
PAIRS["alone"] = [("episodic_recall", "episodic"), ("episodic_recall_r0", "episodic_recall"),
                  ("episodic_recall_h2", "episodic_recall"), ("recall_r0", "episodic"), ("recall_h2_r0", "recall_r0")]



# -- grid 15: the ordered recall world with the writes 4, 16 or 48 neutral events apart

GAP_RECIPES = {k: ORDER_RECIPES[k] for k in ("recall", "recall_nopos", "recall_r0", "recall_nopos_r0")}
GAPS = (4, 16, 48)
SEEDS15 = list(range(1001, 1011))


def derive15() -> list[str]:
    written = []
    for gap in GAPS:
        p = json.loads((HERE / "protocol-m089e-recall-order.json").read_text())
        p["name"] = f"Cadence 0.89 memory on the ordered recall world, the writes {gap} neutral events apart"
        p["world"] = {**p["world"], "gaps": [gap]}
        p["recipes"] = recipes(GAP_RECIPES, p["recipes"]["carried"]["compose"])
        p["arms"] = {"teach_step": copy.deepcopy(p["arms"]["teach_step"])}
        p["seeds"] = {"development": SEEDS15}
        name = f"protocol-m089o-recall-order-gap{gap}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    return written


READINGS15 = {f"recall15-gap{g}": (f"protocol-m089o-recall-order-gap{g}.json", GAP_RECIPES, SEEDS15, "recall_nopos")
              for g in reversed(GAPS)}
PAIRS["gap"] = [("recall", "recall_nopos"), ("recall_r0", "recall_nopos_r0"), ("recall_r0", "recall")]



# -- grid 16: grid 15's gaps on ten more founders, and 96 events apart with room for 128 slots

GAP96_RECIPES = {
    "recall_c128": ({"recall": True, "recall_capacity": 128}, "the recall memory, 128 slots"),
    "recall_r0_c128": ({"recall": True, "recall_capacity": 128, "recall_recency": 0.0},
                       "the recall memory, 128 slots, recency 0"),
    "recall_nopos_r0_c128": ({"recall": True, "recall_capacity": 128, "recall_recency": 0.0, "recall_position": 0},
                             "128 slots, recency 0, no position term"),
}
SEEDS16 = list(range(1011, 1021))


def derive16() -> list[str]:
    written = []
    for gap in GAPS:
        p = json.loads((HERE / f"protocol-m089o-recall-order-gap{gap}.json").read_text())
        p["name"] += ", ten more founders"
        p["seeds"] = {"development": SEEDS16}
        name = f"protocol-m089p-recall-order-gap{gap}.json"
        (HERE / name).write_text(json.dumps(p, indent=1) + "\n")
        written.append(name)
    p = json.loads((HERE / "protocol-m089o-recall-order-gap48.json").read_text())
    p["name"] = "Cadence 0.89 memory on the ordered recall world, the writes 96 neutral events apart, 128 slots"
    p["world"] = {**p["world"], "gaps": [96]}
    p["recipes"] = recipes(GAP96_RECIPES, p["recipes"]["recall"]["compose"] | {"recall": False})
    p["seeds"] = {"development": SEEDS15 + SEEDS16}
    (HERE / "protocol-m089p-recall-order-gap96.json").write_text(json.dumps(p, indent=1) + "\n")
    written.append("protocol-m089p-recall-order-gap96.json")
    return written


READINGS16 = {
    "recall16-gap96": ("protocol-m089p-recall-order-gap96.json", GAP96_RECIPES, SEEDS15 + SEEDS16, "recall_nopos_r0_c128"),
    **{f"recall16-gap{g}": (f"protocol-m089p-recall-order-gap{g}.json", GAP_RECIPES, SEEDS16, "recall_nopos")
       for g in reversed(GAPS)},
}
PAIRS["gap96"] = [("recall_r0_c128", "recall_nopos_r0_c128"), ("recall_c128", "recall_r0_c128")]



# -- grid 17: the position term on the hidden view with 160 fresh founders, corrected arms

HIDDEN17_RECIPES = {k: VIEW3_RECIPES[k] for k in ("recall", "recall_nopos", "episodic_recall", "episodic_recall_nopos")}
HIDDEN17_ARMS = {k: VIEW_ARMS[k] for k in ("corrective_step_120", "corrective_step_480")}
SEEDS17 = list(range(202081, 202241))


def derive17() -> list[str]:
    p = json.loads((HERE / "protocol-m089-view-hidden.json").read_text())
    p["name"] = "Cadence 0.89 memory on the hidden view: the position term on 160 fresh founders"
    p["recipes"] = recipes(HIDDEN17_RECIPES, BASE)
    p["arms"] = copy.deepcopy(HIDDEN17_ARMS)
    p["seeds"] = {"screen": SEEDS17, "development": SEEDS17}
    (HERE / "protocol-m089q-view-hidden.json").write_text(json.dumps(p, indent=1) + "\n")
    return ["protocol-m089q-view-hidden.json"]


READINGS17 = {"view17-hidden": ("protocol-m089q-view-hidden.json", HIDDEN17_RECIPES, SEEDS17, "recall_nopos")}
PAIRS["hidden17"] = [("recall", "recall_nopos"), ("episodic_recall", "episodic_recall_nopos")]


if __name__ == "__main__":
    command = sys.argv[1]
    if len(sys.argv) > 3:
        use_grid(sys.argv[3])
    if command == "derive":
        print("\n".join(derive()))
        print("\n".join(derive2()))
        print("\n".join(derive3()))
        print("\n".join(derive4()))
        print("\n".join(derive5()))
        print("\n".join(derive6()))
        print("\n".join(derive7()))
        print("\n".join(derive8()))
        print("\n".join(derive9()))
        print("\n".join(derive10()))
        print("\n".join(derive11()))
        print("\n".join(derive12()))
        print("\n".join(derive13()))
        print("\n".join(derive14()))
        print("\n".join(derive15()))
        print("\n".join(derive16()))
        print("\n".join(derive17()))
    elif command == "jobs":
        jobs(Path(sys.argv[2]))
    elif command == "analyze":
        analyze(Path(sys.argv[2]))
        contrasts(Path(sys.argv[2]))
        by_condition(Path(sys.argv[2]))
    else:
        raise SystemExit(__doc__)

