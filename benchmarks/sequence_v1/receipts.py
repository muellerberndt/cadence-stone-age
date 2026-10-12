"""Source and environment custody for a run: what code ran, where, with which settings.

A library version alone is not a receipt. The manifest binds every imported Cadence source
file by digest, the instrument's own files and Git state, the platform and numerical
environment, the protocol digest, every seed stream and the resources used.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
THREAD_VARIABLES = (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def tree_digest(root: Path, pattern: str = "*.py") -> dict[str, Any]:
    files = {
        str(path.relative_to(root)): sha256_file(path)
        for path in sorted(root.rglob(pattern))
        if "__pycache__" not in path.parts
    }
    return {"root": str(root), "files": files, "digest": hashlib.sha256(canonical(files)).hexdigest()}


def git_state(path: Path) -> dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(path), *args], capture_output=True, text=True, check=False
        ).stdout.strip()

    head = run("rev-parse", "HEAD")
    if not head:
        return {"repository": None}
    diff = run("diff", "HEAD", "--", ".")
    return {
        "repository": run("rev-parse", "--show-toplevel"),
        "head": head,
        "dirty": bool(run("status", "--porcelain", "--", ".")),
        "diff_sha256": hashlib.sha256(diff.encode()).hexdigest(),
    }


def cadence_identity(wheel_sha256: str | None = None) -> dict[str, Any]:
    import cadence  # noqa: PLC0415
    import numpy  # noqa: PLC0415

    package = Path(cadence.__file__).resolve().parent
    identity = {
        "version": getattr(cadence, "__version__", None),
        "package": tree_digest(package),
        "git": git_state(package),
        "wheel_sha256": wheel_sha256,
        "numpy": numpy.__version__,
    }
    try:
        from importlib.metadata import distribution  # noqa: PLC0415

        dist = distribution("cadence-net")
        identity["distribution"] = {"version": dist.version, "location": str(dist.locate_file(""))}
    except Exception:  # noqa: BLE001 - a source tree on PYTHONPATH has no distribution
        identity["distribution"] = None
    return identity


def environment() -> dict[str, Any]:
    return {
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "threads": {name: os.environ.get(name) for name in THREAD_VARIABLES},
    }


def peak_rss_bytes() -> int:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    children = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    scale = 1 if sys.platform == "darwin" else 1024  # macOS reports bytes, Linux kibibytes
    return int(max(usage, children) * scale)


class Manifest:
    """Opened at the start of a run and closed with its resources at the end."""

    def __init__(self, *, protocol_sha256: str, argv: list[str], wheel_sha256: str | None) -> None:
        self.started = time.time()
        self.body: dict[str, Any] = {
            "schema": "stone-age-sequence-manifest/1",
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.started)),
            "argv": list(argv),
            "protocol_sha256": protocol_sha256,
            "instrument": {"files": tree_digest(HERE), "git": git_state(HERE)},
            "cadence": cadence_identity(wheel_sha256),
            "environment": environment(),
        }

    def close(self, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        ended = time.time()
        self.body["ended_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ended))
        self.body["wall_seconds"] = round(ended - self.started, 3)
        self.body["peak_rss_bytes"] = peak_rss_bytes()
        if extra:
            self.body.update(extra)
        return self.body
