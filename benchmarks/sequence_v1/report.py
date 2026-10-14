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
from runner import CONTROLS, pair_contrasts, reading_of  # noqa: E402


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
        if arm in ("random", "searcher"):
            greedy = [None]  # the random controls have no greedy reading
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
        if arm in CONTROLS:
            continue
        for mode in ("sampled", "greedy"):
            values = [rate(b["arms"][arm], "trained", mode) for b in bodies]
            for control in ("random", "founder", "searcher"):
                base = [rate(b["arms"].get(control, {}), "trained", mode) for b in bodies]
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


def state_table(recipe: str, bodies: list[dict[str, Any]], protocol: dict[str, Any]) -> list[str]:
    """Per-state greedy accuracy (Will Glynn's reading, cadence-teachers EXP-45/46/48): every
    situation read alone from a reset copy; founders with every situation right; on the weather
    chain the seen-minus-unseen gap, founder-paired."""
    founder = bodies[0]["arms"]["founder"].get("per_state")
    if not founder:
        return []
    sets = [name for name in founder if name != "gap"]
    arms = [a for a in bodies[0]["arms"] if a == "founder" or bodies[0]["arms"][a].get("per_state")]
    phases = ["trained"] + (["withdrawn"] if protocol.get("withdrawal_episodes", 0) > 0 else [])
    samples = "memoryless_success" in founder[sets[0]]
    lines = [f"Per-state greedy accuracy, {recipe}: % [per founder], then founders with every situation right", ""]
    head = ["arm"]
    for phase in phases:
        for name in sets:
            head += [f"{phase} {name}", "all right"]
        if "seen" in sets:
            head.append(f"{phase} gap seen - unseen")
        if samples:
            head.append(f"{phase} memoryless %")
    lines += ["| " + " | ".join(head) + " |", "| " + " | ".join(["---"] * len(head)) + " |"]
    for arm in arms:
        cells = [arm]
        for phase in phases:
            readings = [reading_of(b, arm, phase).get("per_state") for b in bodies]
            if any(r is None for r in readings):
                cells += ["-"] * (2 * len(sets) + ("seen" in sets) + samples)
                continue
            for name in sets:
                cells += [fmt([r[name]["accuracy"] for r in readings]),
                          f"{sum(bool(r[name]['all_right']) for r in readings)}/{len(readings)}"]
            if "seen" in sets:
                c = paired_bootstrap([r["seen"]["accuracy"] for r in readings],
                                     [r["unseen"]["accuracy"] for r in readings])
                cells.append(f"{c['mean_difference'] * 100:+.1f} [{c['bootstrap_95'][0] * 100:+.1f}, "
                             f"{c['bootstrap_95'][1] * 100:+.1f}]")
            if samples:
                cells.append(fmt([r[sets[-1]]["memoryless_success"] for r in readings]))
        lines.append("| " + " | ".join(cells) + " |")
    return lines + [""]


def drift_table(recipe: str, bodies: list[dict[str, Any]], protocol: dict[str, Any]) -> list[str]:
    """Each arm read over its life alone, at every withdrawal checkpoint (Will Glynn's reading
    over time, cadence-teachers EXP-47): per-state accuracy %, founders with every situation
    right, greedy and sampled whole-chain success %."""
    marks = [str(k) for k in protocol.get("withdrawal_checkpoints", [])]
    arms = [a for a in bodies[0]["arms"] if "withdrawal" in bodies[0]["arms"][a]]
    if not marks or not arms:
        return []
    founder = bodies[0]["arms"]["founder"].get("per_state") or {}
    name = "unseen" if "unseen" in founder else "chain"
    columns = ["trained", *marks, "withdrawn"]
    titles = ["taught"] + [f"after {k}" for k in marks] + [f"after {protocol['withdrawal_episodes']}"]
    lines = [f"Over the life alone, {recipe}: per-state % ({name}) / all right / greedy % / sampled %", ""]
    lines += ["| arm | " + " | ".join(titles) + " |", "| " + " | ".join(["---"] * (len(titles) + 1)) + " |"]
    for arm in arms:
        cells = [arm]
        for phase in columns:
            readings = [reading_of(b, arm, phase) for b in bodies]
            if any(not r or not r.get("per_state") for r in readings):
                cells.append("-")
                continue
            accuracy = np.mean([r["per_state"][name]["accuracy"] for r in readings]) * 100
            right = sum(bool(r["per_state"][name]["all_right"]) for r in readings)
            greedy, sampled = (
                np.mean([r["frozen"].get(mode, {}).get("summary", {}).get("success_rate", np.nan)
                         for r in readings]) * 100
                for mode in ("greedy", "sampled")
            )
            cells.append(f"{accuracy:.0f} / {right} / {greedy:.0f} / {sampled:.1f}")
        lines.append("| " + " | ".join(cells) + " |")
    return lines + [""]


def pair_lines(bodies: list[dict[str, Any]], protocol: dict[str, Any]) -> list[str]:
    """The arm pairs a protocol declares, founder-paired at every phase."""
    pairs = pair_contrasts(bodies, protocol)
    if not pairs:
        return []
    lines = ["Declared pairs (percentage points, bootstrap 95% over founders):", ""]
    for key, c in pairs.items():
        lines.append(f"- {key}: {c['mean_difference'] * 100:+.1f} [{c['bootstrap_95'][0] * 100:+.1f}, "
                     f"{c['bootstrap_95'][1] * 100:+.1f}], {c['positive']} up / {c['negative']} down / "
                     f"{c['zero']} equal")
    return lines + [""]


def main(argv: list[str]) -> int:
    for run in map(Path, argv):
        manifest = json.loads((run / "manifest.json").read_text()) if (run / "manifest.json").exists() else {}
        print(f"## {run.name}")
        if manifest:
            print(f"\ncadence {manifest['cadence']['version']}, wheel {str(manifest['cadence']['wheel_sha256'])[:12]}, "
                  f"instrument {manifest['instrument']['git'].get('head', '')[:7]} "
                  f"(dirty {manifest['instrument']['git'].get('dirty')}), {manifest['wall_seconds']:.0f} s, "
                  f"peak {manifest['peak_rss_bytes'] / 2**20:.0f} MiB\n")
        protocol = json.loads((run / "protocol.json").read_text()) if (run / "protocol.json").exists() else {}
        metrics = json.loads((run / "metrics.json").read_text()) if (run / "metrics.json").exists() else {}
        for key, value in metrics.get("overrides", {}).items():  # a development run's own lengths
            if key in ("withdrawal_episodes", "withdrawal_checkpoints", "training_episodes"):
                protocol[key] = value
        for recipe, bodies in founders(run).items():
            print("\n".join(table(recipe, bodies)))
            for part in (state_table, drift_table):
                print("\n".join(part(recipe, bodies, protocol)))
            print("\n".join(pair_lines(bodies, protocol)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
