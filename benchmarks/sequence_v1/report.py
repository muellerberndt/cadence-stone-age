"""Markdown tables of a runner output directory, founder by founder.

    python report.py RUN_DIR [RUN_DIR ...]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from metrics import paired_bootstrap  # noqa: E402


def founders(run: Path) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for path in sorted(run.glob("*/founder-*/founder.json")):
        body = json.loads(path.read_text())
        out.setdefault(body["recipe"], []).append(body)
    return out


def rate(arm: dict[str, Any], phase: str, mode: str, field: str = "success_rate") -> float | None:
    frozen = arm.get("frozen", {}) if phase == "trained" else arm.get("withdrawal", {}).get("frozen", {})
    reading = frozen.get(mode) or (frozen.get("sampled") if mode == "greedy" and "greedy" not in frozen else None)
    if reading is None:
        return None
    return reading["summary"].get(field)


def fmt(values: list[float | None], scale: float = 100.0) -> str:
    if any(v is None for v in values):
        return "-"
    return f"{np.mean(values) * scale:.1f} [{' '.join(f'{v * scale:.0f}' for v in values)}]"


def table(recipe: str, bodies: list[dict[str, Any]]) -> list[str]:
    arms = list(bodies[0]["arms"])
    seeds = [b["seed"] for b in bodies]
    first = "first_choice_accuracy" in json.dumps(bodies[0]["arms"]["random"]["frozen"])
    lines = [f"### {recipe}: founders {', '.join(map(str, seeds))}", ""]
    head = "| arm | sampled % [per founder] | greedy % | "
    head += "first choice sampled % | first choice greedy % | " if first else ""
    head += "withdrawn sampled % | withdrawn greedy % | labels | refused | exhausted |"
    lines += [head, "| " + " | ".join(["---"] * (head.count("|") - 1)) + " |"]
    for arm in arms:
        rows = [b["arms"][arm] for b in bodies]
        greedy = [rate(r, "trained", "greedy") for r in rows]
        if arm == "random":
            greedy = [None]  # uniform random has no greedy reading
        cells = [arm, fmt([rate(r, "trained", "sampled") for r in rows]), fmt(greedy)]
        if first:
            cells += [fmt([rate(r, "trained", "sampled", "first_choice_accuracy") for r in rows]),
                      fmt([rate(r, "trained", "greedy", "first_choice_accuracy") for r in rows])]
        if "withdrawal" in rows[0]:
            cells += [fmt([rate(r, "withdrawn", "sampled") for r in rows]),
                      fmt([rate(r, "withdrawn", "greedy") for r in rows])]
        else:
            cells += ["-", "-"]
        if "training" in rows[0]:
            teaching = [r["training"]["counts"]["teaching"] for r in rows]
            cells += [str(sum(t["labels"] for t in teaching)), str(sum(t["refused"] for t in teaching)),
                      str(sum(t["exhausted"] for t in teaching))]
        else:
            cells += ["-", "-", "-"]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("Founder-paired contrasts (percentage points, bootstrap 95% over founders):")
    lines.append("")
    for arm in arms:
        if arm in ("founder", "random", "oracle"):
            continue
        for mode in ("sampled", "greedy"):
            values = [rate(b["arms"][arm], "trained", mode) for b in bodies]
            for control in ("random", "founder"):
                base = [rate(b["arms"][control], "trained", mode) for b in bodies]
                if any(v is None for v in values + base):
                    continue
                c = paired_bootstrap(values, base)
                lines.append(
                    f"- {arm} {mode} minus {control}: {c['mean_difference'] * 100:+.1f} "
                    f"[{c['bootstrap_95'][0] * 100:+.1f}, {c['bootstrap_95'][1] * 100:+.1f}], "
                    f"{c['positive']} up / {c['negative']} down / {c['zero']} equal"
                )
    lines.append("")
    return lines


def main(argv: list[str]) -> int:
    for run in map(Path, argv):
        manifest = json.loads((run / "manifest.json").read_text()) if (run / "manifest.json").exists() else {}
        print(f"## {run.name}")
        if manifest:
            print(f"\ncadence {manifest['cadence']['version']}, wheel {str(manifest['cadence']['wheel_sha256'])[:12]}, "
                  f"instrument {manifest['instrument']['git'].get('head', '')[:7]} "
                  f"(dirty {manifest['instrument']['git'].get('dirty')}), {manifest['wall_seconds']:.0f} s, "
                  f"peak {manifest['peak_rss_bytes'] / 2**20:.0f} MiB\n")
        for recipe, bodies in founders(run).items():
            print("\n".join(table(recipe, bodies)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
