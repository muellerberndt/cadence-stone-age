"""Causal state probes on copies of a brain.

Every probe works on a copy made by a checkpoint round trip; the living brain, its random
generators and its pending outcome are never touched. A probe reads the policy the brain would
act with at one observation: the drive built as ``act`` builds it, settled with the learner's
own qualification from the stream's warm activity, then the softmax readout. It issues no
action, draws no random number and writes no trace.

Interventions remove one component of the runtime state at a time:

- ``intact``: the copy as it is;
- ``sham``: a second checkpoint round trip, which must read the same as ``intact``;
- ``trace_cleared``: the working trace (``trace``, ``last``, ``cold``) of the stream reset;
- ``activity_cleared``: the settle starts from rest instead of the warm activity;
- ``recall_off``: the associative recall is left out of the drive;
- ``efference_cleared``: the copy of the last command reset (only when the brain has one);
- ``full_reset``: ``Brain.reset``, which clears all of the above transient state together and
  the arousal; it is a broad comparator, never a selective ablation.

``transplant`` copies a declared state set from a donor copy into a recipient copy of the same
acquired weights, for the swap tests of P2.
"""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from typing import Any

import numpy as np

INTERVENTIONS = (
    "intact",
    "sham",
    "trace_cleared",
    "activity_cleared",
    "recall_off",
    "efference_cleared",
    "full_reset",
)
TRACE_FIELDS = ("trace", "last", "cold")


class Copier:
    """Checkpoint round trips in one private directory."""

    def __init__(self, directory: str | Path | None = None) -> None:
        self._owned = directory is None
        self._temp = tempfile.TemporaryDirectory(prefix="sequence-v1-") if directory is None else None
        self.directory = Path(self._temp.name if self._temp is not None else directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.count = 0

    def copy(self, brain: Any) -> Any:
        from cadence import Brain  # noqa: PLC0415

        self.count += 1
        path = self.directory / f"copy-{self.count}.npz"
        brain.save(path)
        copy = Brain.load(path)
        path.unlink()
        return copy

    def close(self) -> None:
        if self._temp is not None:
            self._temp.cleanup()


def state_digest(brain: Any, copier: Copier | None = None) -> str:
    """A digest of everything a checkpoint holds, independent of zip metadata: the sorted
    array names, dtypes, shapes and bytes."""
    own = copier is None
    copier = copier or Copier()
    try:
        copier.count += 1
        path = copier.directory / f"digest-{copier.count}.npz"
        brain.save(path)
        digest = hashlib.sha256()
        with np.load(path, allow_pickle=False) as data:
            for name in sorted(data.files):
                value = np.asarray(data[name])
                digest.update(name.encode())
                digest.update(str(value.dtype).encode())
                digest.update(str(value.shape).encode())
                digest.update(np.ascontiguousarray(value).tobytes())
        path.unlink()
        return digest.hexdigest()
    finally:
        if own:
            copier.close()


def _drive(brain: Any, x: np.ndarray, *, recall: bool) -> np.ndarray:
    if recall:
        return brain.stimulus(x)
    drive = brain.stimulus(x, memory=False)
    if brain.working_memory is not None:
        drive = brain.working_memory.stimulate(drive)
    if brain.efference is not None:
        drive = brain.efference.stimulate(drive)
    return drive


def intervene(brain: Any, intervention: str, copier: Copier) -> tuple[Any, dict[str, Any]]:
    """A copy of ``brain`` with one intervention applied, and how the settle must be read."""
    if intervention not in INTERVENTIONS:
        raise ValueError(f"unknown intervention {intervention!r}")
    copy = copier.copy(brain)
    how = {"recall": True, "warm": True, "applicable": True}
    if intervention == "sham":
        copy = copier.copy(copy)
    elif intervention == "trace_cleared":
        if copy.working_memory is None:
            how["applicable"] = False
        else:
            copy.working_memory.reset(1, rows=np.array([0]))
    elif intervention == "activity_cleared":
        how["warm"] = False
    elif intervention == "recall_off":
        how["applicable"] = copy.hippocampus is not None
        how["recall"] = False
    elif intervention == "efference_cleared":
        if copy.efference is None:
            how["applicable"] = False
        else:
            copy.efference.reset(1, rows=np.array([0]))
    elif intervention == "full_reset":
        copy.reset()
    return copy, how


def read_policy(brain: Any, x: np.ndarray, *, recall: bool = True, warm: Any = True) -> dict[str, Any]:
    """The policy at observation ``x`` without acting: qualified settle, motor readout,
    softmax probabilities at the learner's temperature, greedy choice and its margin.
    ``warm`` is True for the stream's own activity, False for rest, or a donor state."""
    x = np.asarray(x, dtype=np.float64)
    drive = _drive(brain, x, recall=recall)
    if warm is True:
        start = brain._activity()  # noqa: SLF001 - source-bound diagnostic access
    elif warm is False or warm is None:
        start = None
    else:
        start = warm
    try:
        state = brain._qualified(drive, start, operation="act")  # noqa: SLF001
    except RuntimeError as error:
        return {"qualified": False, "error": str(error)}
    motor = np.asarray(state.activation)[0, brain.motor_index]
    probabilities = np.asarray(brain.basal_ganglia.probabilities(state))[0]
    order = np.argsort(-motor, kind="stable")
    margin = float(motor[order[0]] - motor[order[1]]) if len(motor) > 1 else float("inf")
    settlement = dict(brain.last_settlement or {})
    tolerance = float(settlement.get("tolerance", np.nan))
    return {
        "qualified": True,
        "greedy": int(order[0]),
        "margin": margin,
        "undecided": bool(margin < tolerance),
        "tolerance": tolerance,
        "steps": int(settlement.get("steps", -1)),
        "probabilities": [float(v) for v in probabilities],
        "motor": [float(v) for v in motor],
    }


def probe(brain: Any, x: np.ndarray, interventions: tuple[str, ...], copier: Copier) -> dict[str, Any]:
    """Read the policy at ``x`` under each intervention, each on its own copy."""
    readings: dict[str, Any] = {}
    for name in interventions:
        copy, how = intervene(brain, name, copier)
        if not how["applicable"]:
            readings[name] = {"applicable": False}
            continue
        reading = read_policy(copy, x, recall=how["recall"], warm=how["warm"])
        reading["applicable"] = True
        readings[name] = reading
    return readings


def transplant(recipient: Any, donor: Any, fields: tuple[str, ...] = ("working_memory",)) -> Any:
    """Copy the donor's declared stream state into the recipient (both copies of the same
    acquired weights). ``working_memory`` and ``efference`` move ``trace``, ``last`` and
    ``cold``; ``activity`` is returned as the warm state to read the recipient from."""
    warm: Any = True
    for name in fields:
        if name in ("working_memory", "efference"):
            source, target = getattr(donor, name), getattr(recipient, name)
            if source is None or target is None:
                raise ValueError(f"both brains need a {name} to transplant it")
            for field in TRACE_FIELDS:
                setattr(target, field, np.array(getattr(source, field), copy=True))
        elif name == "activity":
            warm = donor._activity()  # noqa: SLF001
        else:
            raise ValueError(f"unknown state set {name!r}")
    return warm


def reseed_actions(brain: Any, seed: int) -> None:
    """Give a copy its own action-sampling stream for a frozen evaluation."""
    brain.basal_ganglia.rng = np.random.default_rng(seed)
