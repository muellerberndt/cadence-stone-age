"""The episodic memory's stores at pixel scale under each key source (protocol-cortex-keys-size.json).

    python key_size.py --protocol protocol-cortex-keys-size.json --key cortex --out size-cortex.json

Builds the declared brain, lives the declared moments on random inputs through ``Brain.live``,
and writes the bytes of the stores, the checkpoint size, the time per moment and the time in
the stores' reads and writes. Random inputs carry no task: nothing here measures behavior.
"""

from __future__ import annotations

import argparse
import json
import resource
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import numpy as np


def store_bytes(memory: Any) -> dict[str, int]:
    out = {name: int(getattr(memory, name).nbytes) for name in ("strength", "consolidated", "mass")}
    if memory.separator is not None:
        out["separator_projection"] = int(memory.separator.projection.nbytes)
        out["separator_mean"] = int(memory.separator.mean.nbytes)
    out["inputs"] = int(len(memory.pre))
    return out


def timed(memory: Any, ledger: dict[str, float]) -> None:
    """Count the seconds and calls of a store's reads and writes."""
    recall, observe = memory.recall, memory.observe

    def reading(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return recall(*args, **kwargs)
        finally:
            ledger["read_seconds"] += time.perf_counter() - start
            ledger["reads"] += 1

    def writing(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return observe(*args, **kwargs)
        finally:
            ledger["write_seconds"] += time.perf_counter() - start
            ledger["writes"] += 1

    memory.recall, memory.observe = reading, writing


def summary(values: list[float]) -> dict[str, float | int]:
    if not values:
        return {"count": 0}
    array = np.asarray(values)
    return {"count": int(len(array)), "mean": float(array.mean()), "median": float(np.median(array)),
            "p90": float(np.percentile(array, 90)), "total": float(array.sum())}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--key", choices=("sensory", "cortex"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    protocol = json.loads(args.protocol.read_text())
    spec = protocol["brain"]
    from cadence import Brain  # noqa: PLC0415
    import cadence  # noqa: PLC0415

    started = time.perf_counter()
    brain = Brain.compose(spec["inputs"], spec["actions"], modules=tuple(spec["modules"]),
                          seed=spec["seed"], memory_key=args.key, **spec["compose"])
    composed = time.perf_counter() - started
    names = ("hippocampus", "context_memory")
    before = {name: store_bytes(getattr(brain, name)) for name in names}
    ledger = {"read_seconds": 0.0, "write_seconds": 0.0, "reads": 0, "writes": 0}
    for name in names:
        timed(getattr(brain, name), ledger)
    rng = np.random.default_rng(12824)
    moments = int(protocol["life"]["moments"])
    seconds: list[float] = []
    modes: list[str] = []
    sweeps: list[int] = []
    learning: list[int] = []
    refusals = 0
    reward: float | None = None
    for _ in range(moments):
        x = rng.random((1, spec["inputs"]))
        start = time.perf_counter()
        try:
            brain.live(x) if reward is None else brain.live(x, reward=[reward])
        except RuntimeError:
            refusals += 1
            seconds.append(time.perf_counter() - start)
            modes.append("refused")
            reward = None
            continue
        seconds.append(time.perf_counter() - start)
        reading = brain.last_arousal
        modes.append(str(reading["mode"]))
        sweeps.append(int(reading["sweeps"]))
        learning.append(int(reading["learning_sweeps"]))
        u = rng.random()
        reward = 1.0 if u < 0.1 else (-1.0 if u < 0.2 else 0.0)
    after = {name: store_bytes(getattr(brain, name)) for name in names}
    for name in names:  # unwrap before saving: the checkpoint holds the stores, not the timers
        memory = getattr(brain, name)
        del memory.recall, memory.observe
    with tempfile.TemporaryDirectory() as directory:
        checkpoint = brain.save(Path(directory) / "brain.npz")
        checkpoint_bytes = checkpoint.stat().st_size
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out = {
        "protocol": str(args.protocol),
        "key": args.key,
        "library": str(Path(cadence.__file__).resolve().parent),
        "compose_seconds": composed,
        "stores_before": before,
        "stores_after": after,
        "separator_bytes": sum(v.get("separator_projection", 0) + v.get("separator_mean", 0)
                               for v in before.values()),
        "checkpoint_bytes": int(checkpoint_bytes),
        "moments": moments,
        "refusals": refusals,
        "seconds": summary(seconds),
        "seconds_routine": summary([s for s, m in zip(seconds, modes) if m == "routine"]),
        "seconds_aroused": summary([s for s, m in zip(seconds, modes) if m == "aroused"]),
        "stores_time": ledger,
        "sweeps": summary([float(v) for v in sweeps]),
        "learning_sweeps": summary([float(v) for v in learning]),
        "routine_moments": modes.count("routine"),
        "peak_rss_bytes": int(usage if sys.platform == "darwin" else usage * 1024),
    }
    args.out.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("key", "separator_bytes", "checkpoint_bytes", "refusals")}
                     | {"mean_seconds": out["seconds"].get("mean")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
