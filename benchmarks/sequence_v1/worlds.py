"""Worlds of the sequence instrument: the V5 COLD chain, the vanished route cue, the COLD
chain under a weather that has nothing to do with it, and the COLD chain seen four ways
(progress hidden, an invisible step, progress visible, two consecutive aliases).

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


# -- the COLD chain under an irrelevant weather (P3)
#
# Adapted from Will Glynn's cadence-teachers, EXP-48 "does 0.83's episodic memory generalize the
# Stone Age chain, or record the taught situations?" (https://github.com/WGlynn/cadence-teachers,
# experiments/EXP-48.md and exp/EXP-48_generalize_or_record.py). His design, kept exactly: three
# weather bits after V5's seven inputs, fixed for an attempt; teaching under the four even-parity
# combinations, testing under the four odd-parity ones, so every single bit value is seen in
# teaching and only the combinations are new.

WEATHER_BITS = 3
WEATHER_SEEN = ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0))  # even parity: taught
WEATHER_UNSEEN = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1))  # odd parity: never taught


def weather_cell(cell: Any) -> tuple[int, ...]:
    """A weather as a tuple of 0/1 bits; an episode's schedule cell or a plain sequence."""
    if isinstance(cell, dict):
        cell = cell["weather"]
    bits = tuple(int(b) for b in cell)
    if len(bits) != WEATHER_BITS or any(b not in (0, 1) for b in bits):
        raise ValueError(f"a weather is {WEATHER_BITS} bits of 0 or 1, got {cell!r}")
    return bits


class WeatherChain(ColdChain):
    """V5's COLD chain whose observation also carries a weather, fixed for the episode and
    irrelevant to every rule: the stage, the required action, the deadline and the pay are
    ColdChain's. A brain that learned "inventory to action" ignores the weather; one that keyed
    what it learned on the whole situation meets new situations under an unseen weather."""

    name = "weather_chain"
    inputs = V5_INPUTS + WEATHER_BITS

    def __init__(self, weather: Any = WEATHER_SEEN[0], **chain: Any) -> None:
        super().__init__(**chain)
        self.weather = weather_cell(weather)

    def observation(self) -> np.ndarray:
        return np.concatenate(
            [super().observation(), np.asarray([self.weather], dtype=np.float64)], axis=1
        )


def weather_schedule(episodes: int, rng: np.random.Generator,
                     weathers: tuple[tuple[int, ...], ...] = WEATHER_SEEN) -> list[dict]:
    """One weather per episode, drawn uniformly and independently from ``weathers`` (EXP-48's
    teaching draw)."""
    return [{"weather": list(weathers[int(rng.integers(len(weathers)))])} for _ in range(episodes)]


def weather_cycle(episodes: int, weathers: tuple[tuple[int, ...], ...] = WEATHER_UNSEEN) -> list[dict]:
    """The evaluation's weathers in turn, episode ``i`` under ``weathers[i % len(weathers)]``
    (EXP-48's test order)."""
    return [{"weather": list(weathers[i % len(weathers)])} for i in range(episodes)]


# -- the COLD chain seen three ways: progress hidden, an invisible step, progress visible
#
# Adapted from Will Glynn's cadence-teachers (https://github.com/WGlynn/cadence-teachers). The
# hidden view is the ambiguous chain Huncho reported on the Stone Age world, as the notebook
# rebuilt it in EXP-56 and EXP-57 (experiments/EXP-56.md, exp/EXP-56_ambiguous_chain_trace.py):
# the two A observations are byte-identical, and so are the two B observations. The invisible
# view is EXP-59's chamber (exp/EXP-59_hold_boundary.py), where the first right action changes
# nothing the brain sees. The visible view is EXP-60's (exp/EXP-60_hold_on_visible_chain.py):
# V5's own inventory, a distinct observation per stage. The consecutive view is the alias
# topology of Huncho's Stone Age V7 series, V7.4 (https://github.com/ali12mahmood12345-boop/
# cadence-stone-age, docs/V7_RESULTS.md): two consecutive A observations, then two consecutive B
# observations, each pair byte-identical; V7.4's archives do not publish its vectors, so A and B
# here are the hidden view's. The rules, the deadline and the pay are ColdChain's; only what the
# brain sees at each stage changes.

VIEW_A = v5_observation(wood=0, stone=0, fire=False)  # EXP-56's OBS_A: the empty inventory
VIEW_B = v5_observation(wood=1, stone=0, fire=False)  # EXP-56's OBS_B
VIEW_C = v5_observation(wood=1, stone=1, fire=False)  # EXP-59's OBS_C
VIEW_D = v5_observation(wood=1, stone=1, fire=True)
CHAIN_VIEWS = {
    "hidden": (VIEW_A, VIEW_B, VIEW_A, VIEW_B),  # stages 1 and 3 look alike, and 2 and 4
    "invisible": (VIEW_A, VIEW_A, VIEW_B, VIEW_C),  # the first right action changes nothing seen
    "visible": (VIEW_A, VIEW_B, VIEW_C, VIEW_D),  # V5's observations, one per stage
    "consecutive": (VIEW_A, VIEW_A, VIEW_B, VIEW_B),  # the first and third right actions change nothing seen
}


class ViewChain(ColdChain):
    """V5's COLD chain whose observation at each stage comes from a declared view.

    The stage, the required action, the deadline and the pay are ColdChain's; a wrong action
    leaves the stage unchanged. ``hidden`` shows A, B, A, B at the four stages, so the brain's
    history has to tell stage 3 from stage 1; ``invisible`` shows A, A, B, C, so the brain's own
    correct first action is the only thing that tells stage 2 from stage 1; ``visible`` shows
    V5's inventory, byte-identical to ColdChain at every stage; ``consecutive`` shows A, A, B, B,
    so the brain's own correct first and third actions are the only things that tell stage 2
    from stage 1 and stage 4 from stage 3. The success observation is never shown to a brain (a
    new episode begins); it is ColdChain's."""

    name = "view_chain"

    def __init__(self, view: str = "hidden", efference: bool = False, **chain: Any) -> None:
        if view not in CHAIN_VIEWS:
            raise ValueError(f"a chain view is one of {sorted(CHAIN_VIEWS)}, got {view!r}")
        super().__init__(**chain)
        self.view = view
        # with ``efference`` the observation also shows the brain's last executed action, one
        # input per action, all zero before the episode's first decision
        self.efference = bool(efference)
        self.inputs = V5_INPUTS + (self.actions if self.efference else 0)
        self.last_action: int | None = None

    def observation(self) -> np.ndarray:
        x = super().observation() if self.success else CHAIN_VIEWS[self.view][self.stage].copy()
        if not self.efference:
            return x
        copy = np.zeros((1, self.actions))
        if self.last_action is not None:
            copy[0, self.last_action] = 1.0
        return np.concatenate([np.atleast_2d(x), copy], axis=1)

    def step(self, action: int) -> Outcome:
        outcome = super().step(action)
        self.last_action = int(action_id(np.asarray([action], dtype=np.int64), self.actions))
        return outcome


def views_distinct(spec: dict[str, Any]) -> bool:
    """Whether every stage of a chain world shows its own observation, so that a stage can be
    read alone from a reset copy."""
    if spec["kind"] != "view_chain":
        return True
    seen = [x.tobytes() for x in CHAIN_VIEWS[spec.get("view", "hidden")]]
    return len(set(seen)) == len(seen)


def chain_situations(spec: dict[str, Any], cell: Any = None) -> list[tuple[int, np.ndarray, int]]:
    """Every stage of a chain world as ``(stage, observation, required action)``: the
    observation the world shows at that stage, reached through its own rules."""
    world = make_world(spec, cell)
    out = []
    while not world.done:
        stage, required = world.stage, world.required()
        out.append((stage, world.observation().copy(), int(required)))
        world.step(required)
    return out


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


def make_world(spec: dict[str, Any], route: Any = None) -> Any:
    """A fresh episode world from a protocol entry; ``route`` is the episode's cell from its
    schedule: the hidden route of a route cue episode, a recall episode's condition, value and
    distractor seed, or the weather of a weather chain episode."""
    kind = spec["kind"]
    if kind == "recall":
        cell = route if isinstance(route, dict) else {"condition": "clean-0", "value": int(route or 0), "seed": 0}
        return Recall(cell["condition"], cell["value"], cell.get("seed", 0),
                      success_reward=spec.get("success_reward", 1.0),
                      failure_reward=spec.get("failure_reward", -1.0),
                      ordered=spec.get("ask") == "order")
    if kind == "cold_chain":
        return ColdChain(
            deadline=spec.get("deadline", V5_DEADLINE),
            success_reward=spec.get("success_reward", V5_SUCCESS),
            failure_reward=spec.get("failure_reward", V5_FAILURE),
        )
    if kind == "view_chain":
        return ViewChain(
            spec.get("view", "hidden"),
            efference=bool(spec.get("efference", False)),
            deadline=spec.get("deadline", V5_DEADLINE),
            success_reward=spec.get("success_reward", V5_SUCCESS),
            failure_reward=spec.get("failure_reward", V5_FAILURE),
        )
    if kind == "weather_chain":
        # a probe for the alphabet and the input width passes no cell: the first taught weather
        weather = WEATHER_SEEN[0] if route is None or isinstance(route, int) else route
        return WeatherChain(
            weather,
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


# -- recall: keep a written value, revise it when a later WRITE arrives, answer at QUERY

RECALL_START, RECALL_WRITE, RECALL_NEUTRAL, RECALL_DISTRACTOR, RECALL_QUERY = range(5)
RECALL_PAYLOAD = slice(5, 9)
RECALL_INPUTS = 9
RECALL_TOKENS = np.array([[1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0]])
RECALL_CONDITIONS = (
    "clean-0", "clean-1", "clean-2", "distractor-1", "distractor-2", "replacement", "order-latest",
)
# the ordered recall world (``"ask": "order"``): two values written, then a query for the first or
# the latest, the first asked through a marker of its own at input RECALL_QUERY_FIRST
RECALL_QUERY_FIRST = RECALL_INPUTS
ORDER_CONDITIONS = ("ask-latest", "ask-first", "ask-latest-gap", "ask-first-gap")


def recall_events(condition: str, value: int, seed: int, width: int = RECALL_INPUTS) -> list[np.ndarray]:
    """The observations of one recall episode; the value asked at QUERY is ``value``, the
    latest written one (in the ordered world the first or the latest, as its query asks).
    Distractors carry a small random payload under their own marker."""
    rng = np.random.default_rng(seed)

    def marker(index: int, payload: np.ndarray | None = None) -> np.ndarray:
        x = np.zeros((1, width))
        x[0, index] = 1.0
        if payload is not None:
            x[0, RECALL_PAYLOAD] = payload
        return x

    events = [marker(RECALL_START)]
    if condition in ORDER_CONDITIONS or condition.startswith(("ask-first-gap", "ask-latest-gap")):
        if width <= RECALL_QUERY_FIRST:
            raise ValueError("an ordered recall condition needs the ordered world's query marker")
        first = condition.startswith("ask-first")
        # "-gap" puts one neutral event between the writes, "-gapK" puts K
        tail = condition.rpartition("-gap")[2] if "-gap" in condition else None
        gap = [marker(RECALL_NEUTRAL)] * (0 if tail is None else int(tail or 1))
        writes = [RECALL_TOKENS[value], RECALL_TOKENS[1 - value]] if first else [RECALL_TOKENS[1 - value], RECALL_TOKENS[value]]
        events += [marker(RECALL_WRITE, writes[0]), *gap, marker(RECALL_WRITE, writes[1]), marker(RECALL_NEUTRAL)]
        events.append(marker(RECALL_QUERY_FIRST if first else RECALL_QUERY))
        return events
    kind, _, count = condition.partition("-")
    if kind in ("clean", "distractor"):
        events.append(marker(RECALL_WRITE, RECALL_TOKENS[value]))
        for _ in range(int(count)):
            if kind == "distractor":
                events.append(marker(RECALL_DISTRACTOR, rng.uniform(-0.25, 0.25, 4)))
            else:
                events.append(marker(RECALL_NEUTRAL))
    elif condition == "replacement":
        events += [marker(RECALL_WRITE, RECALL_TOKENS[1 - value]), marker(RECALL_NEUTRAL),
                   marker(RECALL_WRITE, RECALL_TOKENS[value]), marker(RECALL_NEUTRAL)]
    elif condition == "order-latest":
        events += [marker(RECALL_WRITE, RECALL_TOKENS[1 - value]),
                   marker(RECALL_WRITE, RECALL_TOKENS[value]), marker(RECALL_NEUTRAL)]
    else:
        raise ValueError(f"unknown recall condition {condition!r}")
    events.append(marker(RECALL_QUERY))
    return events


class Recall:
    """One recall episode: observation events whose actions the world ignores, then the QUERY
    decision, paid ``success_reward`` for the latest written value and ``failure_reward``
    otherwise. The asked value is a scorer field; no input carries it after its WRITE."""

    name = "recall"
    actions = 2
    inputs = RECALL_INPUTS
    stages = 1

    def __init__(self, condition: str, value: int, seed: int = 0, *,
                 success_reward: float = 1.0, failure_reward: float = -1.0, ordered: bool = False) -> None:
        if value not in (0, 1):
            raise ValueError("value is 0 or 1")
        self.condition, self.value = condition, int(value)
        self.inputs = RECALL_INPUTS + 1 if ordered else RECALL_INPUTS
        self.events = recall_events(condition, self.value, seed, self.inputs)
        self.success_reward, self.failure_reward = float(success_reward), float(failure_reward)
        self.event = 0
        self.stage = 0
        self.decisions = 0
        self.deadline = 1
        self.done = False
        self.success = False

    def required(self) -> int | None:
        return self.value if self.event == len(self.events) - 1 and not self.done else None

    def observation(self) -> np.ndarray:
        return self.events[min(self.event, len(self.events) - 1)].copy()

    def step(self, action: int) -> Outcome:
        if self.done:
            raise RuntimeError("the episode has ended; start a new world")
        index = action_id(np.asarray([action], dtype=np.int64), self.actions)
        if self.event < len(self.events) - 1:
            self.event += 1
            return Outcome(0.0, False, False, False, None, 0, 0, "ignored", decision=False)
        self.decisions = 1
        self.done = True
        self.success = index == self.value
        self.stage = int(self.success)
        return Outcome(
            reward=self.success_reward if self.success else self.failure_reward,
            done=True, success=self.success, advanced=self.success, required=self.value,
            stage_before=0, stage_after=self.stage,
            reason="success" if self.success else "wrong", decision=True,
        )


def recall_schedule(episodes: int, rng: np.random.Generator,
                    conditions: tuple[str, ...] = RECALL_CONDITIONS) -> list[dict]:
    """Balanced blocks: every condition with both values once per block, shuffled; each
    episode has its own distractor seed."""
    out: list[dict] = []
    while len(out) < episodes:
        block = [{"condition": c, "value": v} for c in conditions for v in (0, 1)]
        rng.shuffle(block)
        for cell in block:
            cell["seed"] = int(rng.integers(2**31))
        out.extend(block)
    return out[:episodes]
