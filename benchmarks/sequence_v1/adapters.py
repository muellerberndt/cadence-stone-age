"""Brain adapters with explicit action and outcome custody.

Every action the brain issues gets an identity in a ledger. The world's outcome for that
action is delivered to the brain exactly once, together with the next observation, and is
never attached to another action. A caregiver label names the action for the observation the
brain is shown now; it never relabels an action already executed.

``StepAdapter`` is the historical control (``Brain.step``: learn from every outcome, optional
teacher on the current observation). ``LiveAdapter`` is the continuing animal life
(``Brain.live``: calm routine answers greedily and learns nothing; surprise arouses the brain,
which then samples and learns). ``Brain.live`` takes no teacher; a protocol that combines live
with a caregiver label has to declare an ordering first, so the adapter refuses one.

A life ends at a declared seam: the last executed action's outcome is held in a
``PendingOutcome`` beside the checkpoint instead of being delivered with a next observation
whose action would then be discarded. ``resume`` delivers it exactly once.

An adapter may install a ``context_rules`` rule on its brain for the whole life; every record
then carries the rule's judgment of the previous decision.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np

from context_rules import ContextRule
from worlds import action_id


class CustodyError(RuntimeError):
    """An outcome was about to be delivered twice, to no action, or to the wrong action."""


@dataclass
class PendingOutcome:
    """An executed action's outcome held at a life seam, owed to the brain exactly once."""

    ledger_id: int
    reward: float
    done: bool
    decision_id: int | None = None
    delivered: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Ledger:
    """Issued action identities and the outcomes consumed for them."""

    issued: int = 0
    outstanding: int | None = None
    consumed: list[int] = field(default_factory=list)

    def issue(self) -> int:
        if self.outstanding is not None:
            raise CustodyError(f"action {self.outstanding} still owns an outcome")
        self.issued += 1
        self.outstanding = self.issued
        return self.issued

    def consume(self, ledger_id: int) -> None:
        if self.outstanding is None or ledger_id != self.outstanding:
            raise CustodyError(
                f"outcome for action {ledger_id} but action {self.outstanding} owns the next one"
            )
        if ledger_id in self.consumed:
            raise CustodyError(f"action {ledger_id} already received its outcome")
        self.consumed.append(ledger_id)
        self.outstanding = None

    def replace(self) -> None:
        """A refused answer after an accepted outcome: the retried action is a new identity."""
        self.outstanding = None


def _plain(mapping: Any) -> dict[str, Any]:
    if mapping is None:
        return {}
    out: dict[str, Any] = {}
    for key, value in dict(mapping).items():
        if isinstance(value, (np.floating, np.integer)):
            value = value.item()
        elif isinstance(value, tuple):
            value = [v.item() if isinstance(v, (np.floating, np.integer)) else v for v in value]
        out[str(key)] = value
    return out


def readout(brain: Any) -> dict[str, Any]:
    """The settled motor readout the last action was chosen from: activations, the
    greedy margin, the sampling probabilities and the qualified tolerance."""
    agent = getattr(brain, "basal_ganglia", None)
    state = getattr(agent, "state", None)
    if state is None or not hasattr(brain, "motor_index"):
        return {}
    motor = np.asarray(state.activation)[0, brain.motor_index]
    order = np.argsort(-motor, kind="stable")
    probabilities = np.asarray(agent.probabilities(state))[0]
    settlement = _plain(getattr(brain, "last_settlement", None))
    tolerance = settlement.get("tolerance")
    margin = float(motor[order[0]] - motor[order[1]]) if len(motor) > 1 else float("inf")
    return {
        "motor": [float(v) for v in motor],
        "probabilities": [float(v) for v in probabilities],
        "margin": margin,
        "tolerance": tolerance,
        # a winner closer than the solve tolerance is not decided by the equations
        "undecided": bool(tolerance is not None and margin < float(tolerance)),
    }


class Adapter:
    """Shared custody and records; subclasses define how the brain is called."""

    name = "adapter"

    def __init__(self, brain: Any, actions: int, *, retries: int = 1, context_rule: str = "none") -> None:
        self.brain = brain
        self.rule = ContextRule(brain, context_rule)
        self.actions = int(actions)
        self.retries = int(retries)
        self.ledger = Ledger()
        self.current: int | None = None  # ledger id of the action awaiting its outcome
        self.refusals = 0
        self.teaching_refusals = 0
        self._last_offer: tuple[float, bool, int | None] = (0.0, False, None)

    # subclass hooks
    def _first(self, x: np.ndarray) -> Any:
        raise NotImplementedError

    def _feedback(self, x: np.ndarray, reward: float, done: bool, teacher: int | None) -> Any:
        raise NotImplementedError

    def _answer_only(self, x: np.ndarray) -> Any:
        raise NotImplementedError

    def _accepted(self) -> bool:
        """Whether the outcome just submitted was taken (it no longer owns the brain)."""
        raise NotImplementedError

    def _report(self) -> dict[str, Any]:
        return {}

    # custody
    def first(self, x: np.ndarray) -> tuple[int, dict[str, Any]]:
        if self.current is not None:
            raise CustodyError("an action awaits its outcome; deliver it before a new first act")
        out = self._call(lambda: self._first(x), lambda: self._first(x))
        return self._issued(out)

    def next(
        self, x: np.ndarray, *, reward: float, done: bool, teacher: int | None = None
    ) -> tuple[int, dict[str, Any]]:
        if self.current is None:
            raise CustodyError("no executed action owns this outcome")
        if teacher is not None:
            teacher = action_id(np.asarray([teacher], dtype=np.int64), self.actions)
        owner = self.current
        refused = 0
        self._last_offer = (float(reward), bool(done), teacher)
        try:
            out = self._feedback(x, float(reward), bool(done), teacher)
        except Exception as error:  # noqa: BLE001 - classified below, then re-raised if unknown
            out, refused = self._recover(error, x, owner)
        else:
            self.ledger.consume(owner)
        index, record = self._issued(out)
        record["refused_attempts"] = refused
        return index, record

    def hold(self, reward: float, done: bool) -> PendingOutcome:
        """End the life at a seam: the last action's outcome is held, not delivered."""
        if self.current is None:
            raise CustodyError("no executed action owns an outcome to hold")
        return PendingOutcome(self.current, float(reward), bool(done), self._decision())

    def resume(self, seam: PendingOutcome, x: np.ndarray) -> tuple[int, dict[str, Any]]:
        """Continue a life from its seam: deliver the held outcome once with ``x``."""
        if seam.delivered:
            raise CustodyError("this seam's outcome was delivered already")
        self.current = self.ledger.outstanding = seam.ledger_id
        self.ledger.issued = max(self.ledger.issued, seam.ledger_id)
        seam.delivered = True
        return self.next(x, reward=seam.reward, done=seam.done)

    def _decision(self) -> int | None:
        return None

    def _call(self, call: Any, retry: Any) -> Any:
        attempts = 0
        while True:
            try:
                return call()
            except RuntimeError as error:
                if "settle" not in str(error) or attempts >= self.retries:
                    raise
                attempts += 1
                self.refusals += 1
                call = retry

    def _recover(self, error: Exception, x: np.ndarray, owner: int) -> tuple[Any, int]:
        from cadence.learning import LearningPhaseError  # noqa: PLC0415 - only on failure

        if isinstance(error, LearningPhaseError):
            # the outcome was learned; the caregiver's lesson was refused: act without it
            self.teaching_refusals += 1
            self.ledger.consume(owner)
            return self._call(lambda: self._answer_only(x), lambda: self._answer_only(x)), 1
        if isinstance(error, ValueError) and "feedback was accepted" in str(error):
            # live took the outcome but its arousal could not update: answer without it
            self.refusals += 1
            self.ledger.consume(owner)
            return self._call(lambda: self._answer_only(x), lambda: self._answer_only(x)), 1
        if not isinstance(error, RuntimeError) or "settle" not in str(error):
            raise error
        self.refusals += 1
        if self._accepted():
            # outcome taken, answer refused: retry the answer only, never the outcome
            self.ledger.consume(owner)
            return self._call(lambda: self._answer_only(x), lambda: self._answer_only(x)), 1
        # nothing changed: the same outcome may be offered again, a bounded number of times
        for attempt in range(1, self.retries + 1):
            try:
                out = self._feedback_again(x)
            except RuntimeError as again:
                if "settle" not in str(again):
                    raise
                self.refusals += 1
                if self._accepted():
                    self.ledger.consume(owner)
                    return self._call(
                        lambda: self._answer_only(x), lambda: self._answer_only(x)
                    ), attempt + 1
                continue
            self.ledger.consume(owner)
            return out, attempt
        raise CustodyError(
            "the brain refused the outcome itself; the protocol stops this life"
        ) from error

    def _feedback_again(self, x: np.ndarray) -> Any:
        """Offer the refused outcome once more; set by ``next`` before the first attempt."""
        reward, done, teacher = self._last_offer
        return self._feedback(x, reward, done, teacher)

    def _issued(self, out: Any) -> tuple[int, dict[str, Any]]:
        index = action_id(out, self.actions)
        self.current = self.ledger.issue()
        record = {"ledger_id": self.current, "action": index}
        record.update(self._report())
        if self.rule.rule != "none":
            record["context_rule"] = dict(self.rule.last)
        return index, record


class StepAdapter(Adapter):
    """``Brain.step``: the outcome of the previous action, then an optional label for the
    observation shown now, then the next action, all in one call."""

    name = "step"

    def _first(self, x: np.ndarray) -> Any:
        return self.brain.step(x)

    def _feedback(self, x: np.ndarray, reward: float, done: bool, teacher: int | None) -> Any:
        return self.brain.step(
            x,
            reward=np.asarray([reward], dtype=np.float64),
            done=np.asarray([done], dtype=bool),
            teacher=None if teacher is None else np.asarray([teacher], dtype=np.int64),
        )

    def _answer_only(self, x: np.ndarray) -> Any:
        return self.brain.act(x)

    def _accepted(self) -> bool:
        return not bool(self.brain.pending_feedback)

    def _report(self) -> dict[str, Any]:
        record: dict[str, Any] = {"learning": _plain(getattr(self.brain, "last_learning", None))}
        record["settlement"] = _plain(getattr(self.brain, "last_settlement", None))
        record.update(readout(self.brain))
        return record


class LiveAdapter(Adapter):
    """``Brain.live``: one continuing stream; the outcome is reported under the action's
    ``decision_id`` so a late or repeated outcome is refused before anything changes."""

    name = "live"

    def __init__(self, brain: Any, actions: int, *, retries: int = 1, context_rule: str = "none") -> None:
        super().__init__(brain, actions, retries=retries, context_rule=context_rule)
        self._owner_decision: int | None = None

    def _first(self, x: np.ndarray) -> Any:
        return self.brain.live(x)

    def _feedback(self, x: np.ndarray, reward: float, done: bool, teacher: int | None) -> Any:
        if teacher is not None:
            raise ValueError(
                "Brain.live takes no teacher; declare a caregiver ordering before combining them"
            )
        return self.brain.live(
            x,
            reward=np.asarray([reward], dtype=np.float64),
            done=np.asarray([done], dtype=bool),
            decision_id=self._owner_decision,
        )

    def _answer_only(self, x: np.ndarray) -> Any:
        return self.brain.live(x)

    def _accepted(self) -> bool:
        return self.brain.decision_id != self._owner_decision

    def _decision(self) -> int | None:
        return self._owner_decision

    def _issued(self, out: Any) -> tuple[int, dict[str, Any]]:
        index, record = super()._issued(out)
        self._owner_decision = self.brain.decision_id
        record["decision_id"] = self._owner_decision
        return index, record

    def resume(self, seam: PendingOutcome, x: np.ndarray) -> tuple[int, dict[str, Any]]:
        self._owner_decision = seam.decision_id
        return super().resume(seam, x)

    def _report(self) -> dict[str, Any]:
        record: dict[str, Any] = {"arousal": _plain(getattr(self.brain, "last_arousal", None))}
        record["learning"] = _plain(getattr(self.brain, "last_learning", None))
        record["settlement"] = _plain(getattr(self.brain, "last_settlement", None))
        record.update(readout(self.brain))
        return record


ADAPTERS = {"step": StepAdapter, "live": LiveAdapter}
