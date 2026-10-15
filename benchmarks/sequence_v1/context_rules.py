"""Instrument-level rules for which decisions enter the episodic memory's temporal context.

With ``Brain.compose(..., memory_choice=True)`` and ``memory_context`` above zero, each choice
is keyed by the stream's temporal context: the observation with the fading trace of what the
stream saw and did before, which the library advances after every decision. A rule here
"holds" a decision: before the next decision is keyed, it restores the context to its value
before the held decision, so the held decision never enters a key. A caregiver's label shown
with the next observation is keyed after the rule, as the next decision is.

- ``none``: the library as it is.
- ``hold``: hold every decision after which the observation is unchanged. This is the rule of
  Will Glynn's cadence-teachers, EXP-56 and EXP-57 (https://github.com/WGlynn/cadence-teachers,
  exp/EXP-56_ambiguous_chain_trace.py, ``Trace``), and the rule the library's replay path
  applies to its own path (``Brain._extend_paths``).
- ``hold_td``: hold such a decision only when the outcome that answered it was a failure by
  the brain's critic: a signed temporal-difference error below zero, the reward plus the
  discounted value of the state the stream settled into, less the value the critic forecast
  when the decision was chosen. The queued EXP-63 of the same notebook proposed an outcome
  gate; this is one declared signal for it. When ``learn`` delivers the outcome, the error is
  the one ``learn`` computed, with the critic before its update. In a frozen reading no
  outcome is delivered: the error is read from the frozen critic with a zero reward, the pay
  of the chain worlds inside an attempt.

A rule never acts across the end of an attempt or a ``reset``: a context the library cleared
or replaced since the last decision stays as it is. Rules only read and restore the stream's
``_context``; they change no parameter, record or random state. Installing a rule on a brain
replaces the rule installed before it, and ``none`` removes it.
"""

from __future__ import annotations

from typing import Any

import numpy as np

RULES = ("none", "hold", "hold_td")


class ContextRule:
    """One rule installed on one brain: it wraps the brain's ``learn`` and ``_choose``."""

    def __init__(self, brain: Any, rule: str = "none") -> None:
        if rule not in RULES:
            raise ValueError(f"a context rule is one of {RULES}, got {rule!r}")
        self.brain = brain
        self.rule = rule
        self.unchanged = 0  # decisions after which the observation was unchanged
        self.held = 0  # of those, the decisions held out of the context
        self.last: dict[str, Any] = {}  # the judgment made since the last decision
        self._pending = False  # a decision awaits its judgment
        self._observation: np.ndarray | None = None
        self._before: np.ndarray | None = None  # the context before the last decision
        self._after: np.ndarray | None = None  # the context the last decision left
        self._value = 0.0  # the critic's forecast when the last decision was chosen
        state = vars(brain)
        for name in ("learn", "_choose"):  # a rule replaces a rule installed before it
            if isinstance(getattr(state.get(name), "__self__", None), ContextRule):
                del state[name]
        if rule != "none":
            self._learn, self._choose = brain.learn, brain._choose
            brain.learn, brain._choose = self.learn, self.choose

    def counts(self) -> dict[str, Any]:
        return {"rule": self.rule, "unchanged": self.unchanged, "held": self.held}

    # the brain's calls

    def learn(self, reward: Any, done: Any, next_observations: Any, **options: Any) -> dict[str, float]:
        agent = self.brain.basal_ganglia
        weights, bias = np.array(agent.w_critic, copy=True), float(agent.b_critic)
        report = self._learn(reward, done, next_observations, **options)
        ended = bool(np.asarray(done).reshape(-1)[0])
        error = None
        if self.rule == "hold_td":
            state = agent.state  # the state the stream settled into, valued by the judging critic
            following = 0.0 if ended else float((state.activation[:, agent.critic_index] @ weights + bias)[0])
            r = float(np.asarray(reward, dtype=float).reshape(-1)[0])
            error = r + float(agent.config.gamma) * following - float(report["value"])
        self._judge(np.asarray(next_observations, dtype=float), ended, error)
        return report

    def choose(self, x: np.ndarray, drive: np.ndarray, free: Any, *, greedy: bool,
               temperature: Any = None) -> np.ndarray:
        agent = self.brain.basal_ganglia
        if self._pending:  # no outcome was delivered since the last decision: a frozen reading
            error = None
            if self.rule == "hold_td":
                error = float(agent.config.gamma) * float(agent.value(free)[0]) - self._value
            self._judge(np.asarray(x, dtype=float), False, error)
        context = self.brain._context
        before = None if context is None else context.copy()
        action = self._choose(x, drive, free, greedy=greedy, temperature=temperature)
        context = self.brain._context
        self._observation = np.array(x, dtype=float, copy=True)
        self._before, self._after = before, None if context is None else context.copy()
        self._value = float(agent.value(free)[0])
        self._pending = True
        return action

    # the rule

    def _judge(self, x: np.ndarray, ended: bool, error: float | None) -> None:
        if not self._pending:
            return
        self._pending = False
        self.last = {"unchanged": False, "held": False, "error": error}
        context = self.brain._context
        if ended or self._after is None or context is None or not np.array_equal(context, self._after):
            return  # the end of an attempt or a reset: never across it
        if self._observation is None or not np.array_equal(x, self._observation):
            return
        self.unchanged += 1
        self.last["unchanged"] = True
        if self.rule == "hold_td" and not (error is not None and error < 0):
            return
        self.brain._context = None if self._before is None else self._before.copy()
        self.held += 1
        self.last["held"] = True
