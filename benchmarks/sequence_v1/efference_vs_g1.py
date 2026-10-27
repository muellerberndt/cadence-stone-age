"""Founder-paired effect of showing the last executed action: grid 11 against grid 1, and the replication pairs of\ngrid 13 (the same founders and arms with and without the action shown)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memory_089 as m  # noqa: E402

root = Path(sys.argv[1])
out = {}
for view in ("hidden", "invisible", "consecutive"):
    for recipe in ("defaults", "recall", "recall_nopos", "episodic", "episodic_recall"):
        for arm in ("corrective_step_120", "corrective_step_480", "natural_live_480"):
            diffs = []
            for s in m.VIEW_SEEDS:
                a = m.read_run(root / "g11" / f"view11-{view}" / recipe / f"s{s}", recipe)
                b = m.read_run(root / "g1" / f"view-{view}" / recipe / f"s{s}", recipe)
                if a and b:
                    diffs.append(a[arm]["sampled"] - b[arm]["sampled"])
            d = np.array(diffs)
            lo, hi = m.bootstrap(d)
            out.setdefault(view, {}).setdefault(recipe, {})[arm] = {
                "founders": len(d), "mean": float(d.mean()), "ci": [lo, hi],
                "up": int((d > 0).sum()), "down": int((d < 0).sum())}
(root / "g11" / "efference-vs-g1.json").write_text(json.dumps(out, indent=1) + "\n")
for view, recs in out.items():
    print("==", view)
    for recipe, arms in recs.items():
        cells = [f"{a} {v['mean']:+.2f}[{v['ci'][0]:+.2f},{v['ci'][1]:+.2f}]{v['up']}/{v['down']}" for a, v in arms.items()]
        print(f"  {recipe}: " + " | ".join(cells))


# grid 13: each view with and without the action, on the replication founders
rep = {}
for view in ("consecutive", "invisible"):
    for recipe in ("recall", "episodic", "episodic_recall"):
        for arm in ("corrective_step_120", "natural_live_480"):
            diffs = []
            for s in m.VIEW13_SEEDS:
                a = m.read_run(root / "g13" / f"view13-{view}-efference" / recipe / f"s{s}", recipe)
                b = m.read_run(root / "g13" / f"view13-{view}" / recipe / f"s{s}", recipe)
                if a and b:
                    diffs.append(a[arm]["sampled"] - b[arm]["sampled"])
            d = np.array(diffs)
            lo, hi = m.bootstrap(d)
            rep.setdefault(view, {}).setdefault(recipe, {})[arm] = {
                "founders": len(d), "mean": float(d.mean()), "ci": [lo, hi],
                "up": int((d > 0).sum()), "down": int((d < 0).sum())}
if (root / "g13").exists():
    (root / "g13" / "efference-pairs.json").write_text(json.dumps(rep, indent=1) + "\n")
    for view, recs in rep.items():
        print("== g13", view)
        for recipe, arms in recs.items():
            cells = [f"{a} {v['mean']:+.2f}[{v['ci'][0]:+.2f},{v['ci'][1]:+.2f}]{v['up']}/{v['down']}" for a, v in arms.items()]
            print(f"  {recipe}: " + " | ".join(cells))
