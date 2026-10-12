"""Worlds of the sequence instrument: the V5 COLD chain and the vanished route cue.

A world defines what is correct independently of the brain. Its observation never carries
the required action, the hidden route, the step count or the remaining deadline; those live
in ``Outcome`` and ``Event`` fields that only the scorer and the caregiver read.

Action identities are explicit integers. An output outside the alphabet is rejected with
``InvalidAction`` instead of being clamped to a legal action.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

V5_ACTIONS = ("GATHER_WOOD", "GATHER_STONE", "CRAFT_FIRE", "WARM_UP", "WAIT")
GATHER_WOOD, GATHER_STONE, CRAFT_FIRE, WARM_UP, WAIT = range(5)
V5_INPUTS = 7
V5_DEADLINE = 10
V5_SUCCESS = 2.0
V5_FAILURE = -1.0


class InvalidAction(ValueError):
    """The brain produced an output that names no action of the world's alphabet."""


def action_id(output: Any, actions: int) -> int:
    """The single action a one-stream brain issued, validated against the alphabet."""
    array = np.asarray(output)
    if array.size != 1:
        raise InvalidAction(f"expected one action for one stream, got shape {array.shape}")
    value = array.reshape(-1)[0]
    if isinstance(value, (bool, np.bool_)) or not np.issubdtype(np.asarray(value).dtype, np.integer):
        raise InvalidAction(f"action must be an integer identity, got {value!r}")
    index = int(value)
    if not 0 <= index < actions:
        raise InvalidAction(f"action {index} outside the alphabet of {actions}")
    return index


def v5_observation(*, wood: int, stone: int, fire: bool, warmth: float = 0.35) -> np.ndarray:
    """V5's seven inputs, byte-for-byte: warmth, wood/stone presence, fire, counts, COLD cue."""
    return np.asarray(
        [
            [
                float(np.clip(warmth, 0.0, 1.0)),
                1.0 if wood >= 1 else 0.0,
                1.0 if stone >= 1 else 0.0,
                1.0 if fire else 0.0,
                min(1.0, wood / 2.0),
                min(1.0, stone / 2.0),
                1.0,
            ]
        ],
        dtype=np.float64,
    )


@dataclass(frozen=True)
class Outcome:
    """What the world did with one executed action. Scorer and caregiver fields included."""

    reward: float
    done: bool
    success: bool
    advanced: bool
    required: int | None  # the action the world needed; never part of the learner's input
    stage_before: int
    stage_after: int
    reason: str  # advance, no_effect, success, timeout, locked, ignored
    decision: bool  # whether the event consumed the decision budget


class ColdChain:
    """V5's COLD chain: GATHER_WOOD, GATHER_STONE, CRAFT_FIRE, WARM_UP in order.

    A wrong action leaves the stage unchanged and spends one decision of the deadline.
    The episode ends on WARM_UP at the fire stage (``success_reward``) or when the deadline
    is spent (``failure_reward``). Every observation is fully determined by the stage, so a
    memoryless stage-aware policy solves the chain; the chamber needs no memory.
    """

    name = "cold_chain"
    actions = len(V5_ACTIONS)
    inputs = V5_INPUTS
    stages = 4

    def __init__(
        self,
        *,
        deadline: int = V5_DEADLINE,
        success_reward: float = V5_SUCCESS,
        failure_reward: float = V5_FAILURE,
    ) -> None:
        if deadline < 1:
            raise ValueError("deadline must be at least one decision")
        self.deadline = int(deadline)
        self.success_reward = float(success_reward)
        self.failure_reward = float(failure_reward)
        self.stage = 0
        self.decisions = 0
        self.done = False
        self.success = False

    def required(self) -> int:
        return (GATHER_WOOD, GATHER_STONE, CRAFT_FIRE, WARM_UP)[self.stage]

    def observation(self) -> np.ndarray:
        wood = 1 if self.stage >= 1 else 0
        stone = 1 if self.stage >= 2 else 0
        fire = self.stage >= 3
        warmth = 0.90 if self.success else 0.35
        return v5_observation(wood=wood, stone=stone, fire=fire, warmth=warmth)

    def step(self, action: int) -> Outcome:
        if self.done:
            raise RuntimeError("the episode has ended; start a new world")
        index = action_id(np.asarray([action], dtype=np.int64), self.actions)
        required = self.required()
        before = self.stage
        advanced = index == required
        reason = "no_effect"
        if advanced:
            self.stage += 1
            reason = "advance"
            if self.stage == self.stages:
                self.success = True
                self.done = True
                reason = "success"
        self.decisions += 1
        if not self.done and self.decisions >= self.deadline:
            self.done = True
            reason = "timeout"
        reward = 0.0
        if self.done:
            reward = self.success_reward if self.success else self.failure_reward
        return Outcome(
            reward=reward,
            done=self.done,
            success=self.success,
            advanced=advanced,
            required=required,
            stage_before=before,
            stage_after=self.stage,
            reason=reason,
            decision=True,
        )


# -- the vanished route cue (P2)

ROUTE_INPUTS = 9  # warmth, wood, stone, fire, wood/2, stone/2, world cue, cue A, cue B
ROUTE_A, ROUTE_B = 0, 1


class RouteCue:
    """A route cue shown once, then identical present observations that need different actions.

    Event 0 shows cue A or B for one observation event; ``neutral`` events follow with the
    cue coordinates at zero. During these events the world ignores the brain's action, pays
    zero and spends no decision. Then the decision phase begins from an empty inventory that
    is byte-identical for both routes. Route A needs wood then stone, route B stone then wood;
    both then need CRAFT_FIRE and WARM_UP. Collecting the other material first ends the
    episode at once with the failure pay (``locked``), so a brain cannot succeed by trying both
    orders; WAIT and other wrong actions spend a decision. The deadline counts decision events
    only. Only the first decision needs the cue: after one correct collection the inventory
    shows the route.

    The hidden route, the required action and the remaining budget are scorer fields; the
    observation carries none of them after the cue event.
    """

    name = "route_cue"
    actions = len(V5_ACTIONS)
    inputs = ROUTE_INPUTS
    stages = 4

    def __init__(
        self,
        route: int,
        *,
        neutral: int = 2,
        deadline: int = V5_DEADLINE,
        success_reward: float = V5_SUCCESS,
        failure_reward: float = V5_FAILURE,
        cue_persists: bool = False,
    ) -> None:
        if route not in (ROUTE_A, ROUTE_B):
            raise ValueError("route is ROUTE_A or ROUTE_B")
        if neutral < 0 or deadline < 1:
            raise ValueError("neutral events are nonnegative and the deadline positive")
        self.route = route
        self.cue_persists = bool(cue_persists)  # the external-register control: the cue stays visible
        self.neutral = int(neutral)
        self.deadline = int(deadline)
        self.success_reward = float(success_reward)
        self.failure_reward = float(failure_reward)
        self.event = 0
        self.stage = 0
        self.decisions = 0
        self.locked = False
        self.done = False
        self.success = False

    @property
    def cue_phase(self) -> bool:
        return self.event <= self.neutral

    def order(self) -> tuple[int, int, int, int]:
        first, second = (
            (GATHER_WOOD, GATHER_STONE) if self.route == ROUTE_A else (GATHER_STONE, GATHER_WOOD)
        )
        return (first, second, CRAFT_FIRE, WARM_UP)

    def required(self) -> int | None:
        if self.cue_phase or self.locked:
            return None
        return self.order()[self.stage]

    def observation(self) -> np.ndarray:
        x = np.zeros((1, ROUTE_INPUTS), dtype=np.float64)
        wood = int(self.stage >= 1 and self.route == ROUTE_A or self.stage >= 2)
        stone = int(self.stage >= 1 and self.route == ROUTE_B or self.stage >= 2)
        fire = self.stage >= 3
        x[0, :7] = v5_observation(
            wood=wood, stone=stone, fire=fire, warmth=0.90 if self.success else 0.35
        )[0]
        if self.event == 0 or self.cue_persists:
            x[0, 7 + self.route] = 1.0
        return x

    def step(self, action: int) -> Outcome:
        if self.done:
            raise RuntimeError("the episode has ended; start a new world")
        index = action_id(np.asarray([action], dtype=np.int64), self.actions)
        if self.cue_phase:
            self.event += 1
            return Outcome(0.0, False, False, False, None, 0, 0, "ignored", decision=False)
        self.event += 1
        before = self.stage
        required = None if self.locked else self.order()[self.stage]
        advanced = required is not None and index == required
        reason = "no_effect"
        if advanced:
            self.stage += 1
            reason = "advance"
            if self.stage == self.stages:
                self.success = True
                self.done = True
                reason = "success"
        elif self.stage == 0 and index in (GATHER_WOOD, GATHER_STONE):
            # the other material first: the route's order can no longer be kept
            self.locked = True
            self.done = True
            reason = "locked"
        self.decisions += 1
        if not self.done and self.decisions >= self.deadline:
            self.done = True
            reason = "timeout"
        reward = 0.0
        if self.done:
            reward = self.success_reward if self.success else self.failure_reward
        return Outcome(
            reward=reward,
            done=self.done,
            success=self.success,
            advanced=advanced,
            required=required,
            stage_before=before,
            stage_after=self.stage,
            reason=reason,
            decision=True,
        )


def make_world(spec: dict[str, Any], route: int | None = None) -> Any:
    """A fresh episode world from a protocol entry; ``route`` is the hidden route of a route
    cue episode, drawn by the caller from a balanced schedule."""
    kind = spec["kind"]
    if kind == "cold_chain":
        return ColdChain(
            deadline=spec.get("deadline", V5_DEADLINE),
            success_reward=spec.get("success_reward", V5_SUCCESS),
            failure_reward=spec.get("failure_reward", V5_FAILURE),
        )
    if kind == "route_cue":
        if route is None:
            raise ValueError("a route cue episode needs its hidden route")
        return RouteCue(
            int(route),
            neutral=spec.get("neutral", 2),
            deadline=spec.get("deadline", V5_DEADLINE),
            success_reward=spec.get("success_reward", V5_SUCCESS),
            failure_reward=spec.get("failure_reward", V5_FAILURE),
            cue_persists=spec.get("cue_persists", False),
        )
    raise ValueError(f"unknown world {kind!r}")


def balanced_routes(episodes: int, rng: np.random.Generator) -> list[int]:
    """Hidden routes in shuffled blocks of two, so every pair of episodes holds A and B."""
    routes: list[int] = []
    while len(routes) < episodes:
        block = [ROUTE_A, ROUTE_B]
        rng.shuffle(block)
        routes.extend(block)
    return routes[:episodes]
