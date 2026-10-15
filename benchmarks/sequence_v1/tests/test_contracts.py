"""Contracts of the sequence instrument: scorer, custody, isolation and continuation.

The spy-brain tests need only NumPy. The tests marked ``cadence`` use a small real
``Brain.compose`` and are skipped when Cadence is not importable.
"""

from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import adapters as ad  # noqa: E402
import metrics as me  # noqa: E402
import runner as ru  # noqa: E402
import worlds as wo  # noqa: E402

try:
    import cadence  # noqa: F401

    HAVE_CADENCE = True
except ImportError:  # pragma: no cover - environment dependent
    HAVE_CADENCE = False

needs_cadence = pytest.mark.skipif(not HAVE_CADENCE, reason="Cadence is not importable")
COLD = {"kind": "cold_chain", "deadline": 10, "success_reward": 2.0, "failure_reward": -1.0}


# -- scorer


def test_uniform_random_exact_value_matches_v5_review() -> None:
    exact = me.uniform_chain_success_exact(5, 4, 10)
    assert abs(float(exact) - 0.1208738816) < 1e-10
    assert abs(me.chain_success([0.2] * 4, 10) - float(exact)) < 1e-12


def test_dynamic_programme_matches_enumeration_of_the_world() -> None:
    deadline = 6
    wins = Fraction(0)
    for sequence in itertools.product(range(5), repeat=deadline):
        world = wo.ColdChain(deadline=deadline)
        for action in sequence:
            if world.done:
                break
            world.step(action)
        if world.success:
            wins += Fraction(1, 5**deadline)
    assert wins == me.uniform_chain_success_exact(5, 4, deadline)
    assert abs(me.chain_success([0.2] * 4, deadline) - float(wins)) < 1e-12


def test_memoryless_fingerprint_model_of_the_review() -> None:
    # seed 42's reset fingerprint in the review: 7.674 percent within ten decisions
    assert abs(me.chain_success([0.727, 0.10, 0.11, 0.163], 10) - 0.07674) < 5e-5


def test_first_passage_sums_to_success() -> None:
    advance = [0.3, 0.5, 0.2, 0.9]
    assert abs(sum(me.first_passage(advance, 10)) - me.chain_success(advance, 10)) < 1e-12


def test_sampled_ceiling_of_the_plan() -> None:
    single = 1 / (1 + 4 * np.exp(-5.5))
    assert abs(me.sampled_ceiling(5, 0.2, -0.1, 1.0, 7) - single**7) < 1e-12
    assert me.sampled_ceiling(5, 0.2, -0.1, 1.0, 7) < 0.90


# -- worlds


def test_cold_chain_rules() -> None:
    world = wo.ColdChain()
    first = world.observation().copy()
    outcome = world.step(wo.WAIT)
    assert outcome.reason == "no_effect" and world.stage == 0 and not outcome.done
    assert np.array_equal(world.observation(), first)
    for action in (wo.GATHER_WOOD, wo.GATHER_STONE, wo.CRAFT_FIRE):
        assert world.step(action).reason == "advance"
    outcome = world.step(wo.WARM_UP)
    assert outcome.success and outcome.done and outcome.reward == 2.0
    with pytest.raises(RuntimeError):
        world.step(wo.WAIT)


def test_cold_chain_timeout_and_v5_observations() -> None:
    world = wo.ColdChain()
    for _ in range(9):
        assert not world.step(wo.WAIT).done
    outcome = world.step(wo.WAIT)
    assert outcome.done and not outcome.success and outcome.reason == "timeout"
    assert outcome.reward == -1.0
    stages = [
        wo.v5_observation(wood=0, stone=0, fire=False),
        wo.v5_observation(wood=1, stone=0, fire=False),
        wo.v5_observation(wood=1, stone=1, fire=False),
        wo.v5_observation(wood=1, stone=1, fire=True),
    ]
    world = wo.ColdChain()
    for stage, expected in enumerate(stages):
        assert np.array_equal(world.observation(), expected), stage
        world.step(world.required())


@pytest.mark.parametrize("bad", [-1, 5, 2.0, True, np.array([1, 2]), "1"])
def test_invalid_outputs_are_rejected_not_clamped(bad: object) -> None:
    with pytest.raises(wo.InvalidAction):
        wo.action_id(bad, 5)


def test_oracle_completes_in_four_and_random_rate_is_near_exact() -> None:
    rows = ru.control_rows("oracle", COLD, episodes=20, seed=1)
    assert all(r["success"] and r["decisions"] == 4 for r in rows)
    rows = ru.control_rows("random", COLD, episodes=20_000, seed=2)
    rate = np.mean([r["success"] for r in rows])
    assert abs(rate - 0.1208738816) < 0.01


def test_route_cue_hides_the_route_after_the_cue() -> None:
    a, b = wo.RouteCue(wo.ROUTE_A), wo.RouteCue(wo.ROUTE_B)
    assert a.observation()[0, 7] == 1.0 and b.observation()[0, 8] == 1.0
    assert not np.array_equal(a.observation(), b.observation())
    for world in (a, b):
        for _ in range(3):  # the cue event and two neutral events
            outcome = world.step(wo.WAIT)
            assert outcome.reason == "ignored" and not outcome.decision and outcome.reward == 0.0
    assert np.array_equal(a.observation(), b.observation())
    assert a.required() == wo.GATHER_WOOD and b.required() == wo.GATHER_STONE
    assert a.decisions == b.decisions == 0


def test_route_cue_locks_a_wrong_first_collection_and_keeps_retries_harmless() -> None:
    world = wo.RouteCue(wo.ROUTE_A, neutral=0)
    world.step(wo.WAIT)  # the cue event
    outcome = world.step(wo.GATHER_STONE)
    assert outcome.done and outcome.reason == "locked" and outcome.reward == -1.0
    world = wo.RouteCue(wo.ROUTE_B, neutral=0)
    world.step(wo.WAIT)
    assert world.step(wo.GATHER_STONE).advanced
    assert world.step(wo.GATHER_STONE).reason == "no_effect"  # a repeat, not a lock
    for action in (wo.GATHER_WOOD, wo.CRAFT_FIRE, wo.WARM_UP):
        outcome = world.step(action)
    assert outcome.success


def test_balanced_routes() -> None:
    routes = wo.balanced_routes(200, np.random.default_rng(0))
    assert len(routes) == 200 and sum(routes) == 100
    assert all(sorted(routes[i : i + 2]) == [0, 1] for i in range(0, 200, 2))


# -- custody with a spy brain


class SpyBrain:
    """Records every call; refuses misuse the way Cadence does; optional injected refusals."""

    def __init__(self, actions: int = 5, seed: int = 0, refuse_answers: int = 0,
                 refuse_outcomes: int = 0) -> None:
        self.rng = np.random.default_rng(seed)
        self.actions = actions
        self.pending = False
        self.calls: list[tuple] = []
        self.outcomes: list[float] = []
        self.labels: list[tuple[str, int]] = []
        self.refuse_answers = refuse_answers
        self.refuse_outcomes = refuse_outcomes
        self.age = 0
        self.last_learning: dict = {}
        self.last_settlement: dict = {}
        self.last_arousal: dict = {}

    @property
    def pending_feedback(self) -> bool:
        return self.pending

    @property
    def decision_id(self) -> int | None:
        return self.age if self.pending else None

    def _answer(self, x: np.ndarray) -> np.ndarray:
        if self.refuse_answers > 0:
            self.refuse_answers -= 1
            raise RuntimeError("brain did not settle within 1 steps; no action issued")
        self.pending = True
        self.age += 1
        return np.asarray([int(self.rng.integers(self.actions))])

    def _outcome(self, reward: np.ndarray | None, done: np.ndarray | None) -> None:
        if reward is None:
            return
        if not self.pending:
            raise RuntimeError("feedback needs a preceding action")
        if self.refuse_outcomes > 0:
            self.refuse_outcomes -= 1
            raise RuntimeError("brain did not settle the forecast")
        self.outcomes.append(float(reward[0]))
        self.pending = False

    def step(self, x, *, reward=None, done=None, teacher=None):  # noqa: ANN001
        self.calls.append(("step", reward is not None, teacher is not None))
        self._outcome(reward, done)
        if teacher is not None:
            self.labels.append((ru.observation_digest(np.asarray(x)), int(teacher[0])))
            self.last_learning = {"demonstrations": 1.0, "demonstration_accepted": 1.0}
        return self._answer(x)

    def live(self, x, *, reward=None, done=None, decision_id=None):  # noqa: ANN001
        self.calls.append(("live", reward is not None, decision_id))
        if decision_id is not None and decision_id != self.decision_id:
            raise ValueError("outcome reported for another action")
        self._outcome(reward, done)
        return self._answer(x)

    def act(self, x, greedy=False):  # noqa: ANN001
        self.calls.append(("act", False, None))
        return self._answer(x)


def _life(adapter: ad.Adapter, caregiver: ru.Caregiver, episodes: int = 30) -> ru.Life:
    return ru.run_life(adapter, COLD, caregiver, episodes, life_id="spy")


@pytest.mark.parametrize("kind", ["none", "grade", "correct"])
def test_every_executed_action_gets_exactly_one_outcome(kind: str) -> None:
    spy = SpyBrain()
    adapter = ad.StepAdapter(spy, 5)
    life = _life(adapter, ru.Caregiver(kind, 4, 8))
    executed = [e for e in life.events]
    # every executed action but the last received its outcome; the last is held at the seam
    assert len(spy.outcomes) == len(executed) - 1
    assert life.counts["outcomes_delivered"] == len(executed) - 1
    assert life.counts["actions_issued"] == len(executed)
    assert life.seam.ledger_id == life.counts["actions_issued"] and not life.seam.delivered
    assert [e["consumed_reward"] for e in executed[:-1]] == spy.outcomes
    assert life.counts["episodes"] == 30


def test_teacher_labels_only_the_current_cue_after_a_guided_nonterminal_mistake() -> None:
    spy = SpyBrain(seed=3)
    life = _life(ad.StepAdapter(spy, 5), ru.Caregiver("correct", 4, 8), episodes=40)
    labelled = [e for e in life.events if e["label"] is not None]
    assert labelled, "the spy makes mistakes, so some labels are expected"
    for event in labelled:
        assert event["guided"] and not event["advanced"] and not event["done"]
        # after a mistake the stage is unchanged, so the label is the same requirement
        assert event["label"] == event["required"]
    for event in life.events:
        if event["label"] is None:
            assert not (event["guided"] and not event["advanced"] and not event["done"])
    assert len(spy.labels) == len(labelled)


def test_grades_only_in_guided_windows_and_never_relabel() -> None:
    spy = SpyBrain(seed=4)
    life = _life(ad.StepAdapter(spy, 5), ru.Caregiver("grade", 4, 8), episodes=40)
    for event in life.events:
        if event["guided"]:
            assert event["grade"] == (0.5 if event["advanced"] else -0.5)
        else:
            assert event["grade"] == 0.0
        assert event["label"] is None
        assert event["consumed_reward"] == event["world_reward"] + event["grade"]
    assert not spy.labels


def test_refused_answer_after_an_accepted_outcome_is_retried_without_the_outcome() -> None:
    spy = SpyBrain()
    adapter = ad.StepAdapter(spy, 5)
    adapter.first(wo.ColdChain().observation())
    spy.refuse_answers = 1
    action, record = adapter.next(wo.ColdChain().observation(), reward=0.0, done=False)
    assert spy.outcomes == [0.0]  # credited once
    assert [c[0] for c in spy.calls] == ["step", "step", "act"]
    assert record["refused_attempts"] == 1 and adapter.refusals == 1
    assert adapter.ledger.consumed == [1]


def test_a_refused_outcome_is_offered_again_a_bounded_number_of_times() -> None:
    spy = SpyBrain(refuse_outcomes=1)
    adapter = ad.LiveAdapter(spy, 5)
    adapter.first(wo.ColdChain().observation())
    adapter.next(wo.ColdChain().observation(), reward=1.0, done=False)
    assert spy.outcomes == [1.0]
    spy2 = SpyBrain(refuse_outcomes=5)
    adapter2 = ad.LiveAdapter(spy2, 5)
    adapter2.first(wo.ColdChain().observation())
    with pytest.raises(ad.CustodyError):
        adapter2.next(wo.ColdChain().observation(), reward=1.0, done=False)
    assert spy2.outcomes == []


def test_live_refuses_a_teacher_and_reports_its_decision_identity() -> None:
    spy = SpyBrain()
    adapter = ad.LiveAdapter(spy, 5)
    _, record = adapter.first(wo.ColdChain().observation())
    assert record["decision_id"] == 1
    with pytest.raises(ValueError):
        adapter.next(wo.ColdChain().observation(), reward=0.0, done=False, teacher=0)
    assert spy.outcomes == []


def test_custody_errors() -> None:
    adapter = ad.StepAdapter(SpyBrain(), 5)
    with pytest.raises(ad.CustodyError):
        adapter.next(wo.ColdChain().observation(), reward=0.0, done=False)
    adapter.first(wo.ColdChain().observation())
    with pytest.raises(ad.CustodyError):
        adapter.first(wo.ColdChain().observation())


def test_seam_delivers_its_outcome_exactly_once() -> None:
    spy = SpyBrain()
    life = _life(ad.StepAdapter(spy, 5), ru.Caregiver("none", 0, 1), episodes=3)
    seam = life.seam
    follow = ad.StepAdapter(spy, 5)
    follow.resume(seam, wo.ColdChain().observation())
    assert spy.outcomes[-1] == seam.reward and seam.delivered
    with pytest.raises(ad.CustodyError):
        follow.resume(seam, wo.ColdChain().observation())


def test_protocol_refuses_live_with_a_teacher(tmp_path: Path) -> None:
    protocol = json.loads((HERE / "protocol.json").read_text())
    protocol["arms"]["bad"] = {"adapter": "live", "caregiver": "correct"}
    path = tmp_path / "protocol.json"
    path.write_text(json.dumps(protocol))
    with pytest.raises(ValueError):
        ru.load_protocol(path)


# -- real Cadence: isolation and continuation


def _small_brain(seed: int = 7):  # noqa: ANN202
    from cadence import Brain

    return Brain.compose(inputs=7, actions=5, modules=(12,), seed=seed, arousal=True)


@needs_cadence
def test_probes_leave_the_living_brain_untouched(tmp_path: Path) -> None:
    import probes as pr

    brain = _small_brain()
    adapter = ad.LiveAdapter(brain, 5)
    ru.run_life(adapter, COLD, ru.Caregiver("none", 0, 1), 3, life_id="probe")
    copier = pr.Copier(tmp_path / "copies")
    before = pr.state_digest(brain, copier)
    rng_before = brain.basal_ganglia.rng.bit_generator.state
    readings = pr.probe(brain, wo.ColdChain().observation(), pr.INTERVENTIONS, copier)
    assert pr.state_digest(brain, copier) == before
    assert brain.basal_ganglia.rng.bit_generator.state == rng_before
    assert readings["sham"]["motor"] == readings["intact"]["motor"]
    assert readings["intact"]["qualified"]
    assert readings["efference_cleared"]["applicable"] is False  # no efference copy composed


@needs_cadence
@pytest.mark.parametrize("adapter_name", ["step", "live"])
def test_saved_seam_continues_exactly_like_the_uninterrupted_life(tmp_path: Path, adapter_name: str) -> None:
    from cadence import Brain

    import probes as pr

    brain = _small_brain(11)
    life = ru.run_life(ad.ADAPTERS[adapter_name](brain, 5), COLD, ru.Caregiver("grade", 4, 8), 4,
                       life_id="a")
    path = tmp_path / "seam.npz"
    brain.save(path)
    seam = json.loads(json.dumps(life.seam.to_dict()))
    loaded = Brain.load(path)
    one = ru.run_life(ad.ADAPTERS[adapter_name](brain, 5), COLD, ru.Caregiver("grade", 4, 8), 3,
                      life_id="b", seam=ad.PendingOutcome(**seam))
    two = ru.run_life(ad.ADAPTERS[adapter_name](loaded, 5), COLD, ru.Caregiver("grade", 4, 8), 3,
                      life_id="b", seam=ad.PendingOutcome(**seam))
    assert [e["action"] for e in one.events] == [e["action"] for e in two.events]
    assert [e["consumed_reward"] for e in one.events] == [e["consumed_reward"] for e in two.events]
    learned_one = [e["learning"].get("td_error") for e in one.events]
    learned_two = [e["learning"].get("td_error") for e in two.events]
    assert learned_one == learned_two
    copier = pr.Copier(tmp_path / "c")
    assert pr.state_digest(brain, copier) == pr.state_digest(loaded, copier)


@needs_cadence
def test_frozen_evaluation_is_isolated_and_seeded(tmp_path: Path) -> None:
    import probes as pr

    brain = _small_brain(13)
    ru.run_life(ad.StepAdapter(brain, 5), COLD, ru.Caregiver("none", 0, 1), 3, life_id="e")
    path = tmp_path / "trained.npz"
    brain.save(path)
    copier = pr.Copier(tmp_path / "c")
    before = pr.state_digest(brain, copier)
    first = ru.evaluate(path, COLD, episodes=6, greedy=False, seed=5)
    again = ru.evaluate(path, COLD, episodes=6, greedy=False, seed=5)
    other = ru.evaluate(path, COLD, episodes=6, greedy=False, seed=6)
    assert first == again
    assert [r["decisions"] for r in first] != [r["decisions"] for r in other] or first != other
    assert pr.state_digest(brain, copier) == before
    greedy = ru.evaluate(path, COLD, episodes=3, greedy=True, seed=5)
    assert greedy == ru.evaluate(path, COLD, episodes=3, greedy=True, seed=99)


def test_visible_cue_control_keeps_the_cue_and_first_choice_metric() -> None:
    world = wo.make_world({"kind": "route_cue", "cue_persists": True}, route=wo.ROUTE_B)
    for _ in range(3):
        world.step(wo.WAIT)
    assert world.observation()[0, 8] == 1.0 and world.observation()[0, 7] == 0.0
    rows = ru.control_rows("oracle", {"kind": "route_cue"}, episodes=10, seed=0,
                           routes=wo.balanced_routes(10, np.random.default_rng(1)))
    assert all(r["success"] for r in rows)
    summary = me.episode_summary(
        [{"success": True, "decisions": 4, "stage_reached": 4, "reason": "success", "route": 0,
          "first_choice": {"action": 0, "required": 0}},
         {"success": False, "decisions": 1, "stage_reached": 0, "reason": "locked", "route": 1,
          "first_choice": {"action": 0, "required": 1}}], 4)
    assert summary["first_choice_accuracy"] == 0.5
    assert summary["first_choice_by_route"] == {"0": 1.0, "1": 0.0}


def test_live_arousal_refusal_after_an_accepted_outcome_answers_without_it() -> None:
    class ArousalFailure(SpyBrain):
        failed = False

        def live(self, x, *, reward=None, done=None, decision_id=None):  # noqa: ANN001
            if reward is not None and not self.failed:
                self.failed = True
                self._outcome(reward, done)  # the outcome is taken
                raise ValueError("feedback was accepted but arousal could not update; retry")
            return super().live(x, reward=reward, done=done, decision_id=decision_id)

    spy = ArousalFailure()
    adapter = ad.LiveAdapter(spy, 5)
    adapter.first(wo.ColdChain().observation())
    _, record = adapter.next(wo.ColdChain().observation(), reward=-1.0, done=False)
    assert spy.outcomes == [-1.0] and record["refused_attempts"] == 1
    assert adapter.ledger.consumed == [1]


def test_guide_labels_every_guided_decision_before_the_brain_acts() -> None:
    spy = SpyBrain(seed=5)
    routes = wo.balanced_routes(20, np.random.default_rng(0))
    life = ru.run_life(ad.StepAdapter(spy, 5), {"kind": "route_cue"}, ru.Caregiver("guide", 4, 8), 20,
                       life_id="guide", routes=routes)
    events = life.events
    for previous, event in zip(events, events[1:]):
        # a label rides with the observation of the event that follows it
        if previous["label"] is not None:
            assert event["kind"] == "decision"
            assert previous["label"] == event["required"]
    labelled_first = [
        e for p, e in zip(events, events[1:])
        if p["label"] is not None and e["stage_before"] == 0 and e["kind"] == "decision"
    ]
    assert labelled_first, "the ambiguous first decision receives labels in guided windows"
    for event in events:
        if event["kind"] == "observe":
            assert event["required"] is None


def test_recall_world_answers_the_latest_written_value_only_at_query() -> None:
    for condition in wo.RECALL_CONDITIONS:
        for value in (0, 1):
            world = wo.make_world({"kind": "recall"}, {"condition": condition, "value": value, "seed": 3})
            while world.required() is None:
                outcome = world.step(1 - value)  # ignored before the query
                assert outcome.reason == "ignored" and not outcome.decision and outcome.reward == 0.0
            query = world.observation()
            assert query[0, wo.RECALL_QUERY] == 1.0 and not query[0, wo.RECALL_PAYLOAD].any()
            outcome = world.step(value)
            assert outcome.done and outcome.success and outcome.reward == 1.0 and outcome.required == value
    world = wo.make_world({"kind": "recall"}, {"condition": "replacement", "value": 1, "seed": 0})
    writes = [x for x in world.events if x[0, wo.RECALL_WRITE] == 1.0]
    assert np.array_equal(writes[-1][0, wo.RECALL_PAYLOAD], wo.RECALL_TOKENS[1])
    assert np.array_equal(writes[0][0, wo.RECALL_PAYLOAD], wo.RECALL_TOKENS[0])


def test_recall_schedule_is_balanced_and_guide_labels_the_query_only() -> None:
    schedule = wo.recall_schedule(28, np.random.default_rng(0))
    cells = {(c["condition"], c["value"]) for c in schedule}
    assert len(cells) == 14 and len(schedule) == 28
    spy = SpyBrain(actions=2, seed=1)
    life = ru.run_life(ad.StepAdapter(spy, 2), {"kind": "recall"}, ru.Caregiver("guide", 1, 0), 28,
                       life_id="recall", routes=schedule)
    labelled = [p for p, e in zip(life.events, life.events[1:]) if p["label"] is not None]
    assert labelled and all(e["kind"] == "decision" for e in
                            [e for p, e in zip(life.events, life.events[1:]) if p["label"] is not None])
    assert life.counts["outcomes_delivered"] == life.counts["actions_issued"] - 1


def test_oracle_and_random_controls_run_on_every_world() -> None:
    schedule = wo.recall_schedule(14, np.random.default_rng(2))
    rows = ru.control_rows("oracle", {"kind": "recall"}, episodes=14, seed=0, routes=schedule)
    assert all(r["success"] for r in rows)
    rows = ru.control_rows("random", {"kind": "recall"}, episodes=14, seed=0, routes=schedule)
    assert all(r["decisions"] == 1 for r in rows)
    routes = wo.balanced_routes(6, np.random.default_rng(0))
    assert all(r["success"] for r in ru.control_rows("oracle", {"kind": "route_cue"}, episodes=6, seed=0, routes=routes))


def test_a_recipe_can_set_the_motor_readout_bias_at_birth_and_nothing_else():
    world = {"kind": "cold_chain", "deadline": 10, "success_reward": 2.0, "failure_reward": -1.0}
    recipe = {"compose": {"modules": [12, 6], "arousal": True}}
    plain = ru.compose(recipe, 3, world, {})
    biased = ru.compose({"compose": {**recipe["compose"], "motor_bias": 0.3}}, 3, world, {})
    motor = np.asarray(biased.motor_index)
    assert np.allclose(biased.brain.bias[motor], 0.3)
    others = np.setdiff1d(np.arange(len(biased.brain.bias)), motor)
    assert np.array_equal(biased.brain.bias[others], plain.brain.bias[others])
    assert np.array_equal(biased.brain.efficacy, plain.brain.efficacy)


def test_an_arm_may_continue_alone_through_another_interface(tmp_path):
    protocol = json.loads((HERE / "protocol-p1-next.json").read_text())
    assert protocol["arms"]["correct_then_live"]["withdrawal_adapter"] == "live"
    protocol["arms"]["correct_then_live"]["withdrawal_adapter"] = "telepathy"
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(protocol))
    with pytest.raises(ValueError, match="withdrawal adapter"):
        ru.load_protocol(path)


# -- tests adapted from Will Glynn's cadence-teachers (https://github.com/WGlynn/cadence-teachers):
#    the never-repeat searcher (EXP-45), per-state reading (EXP-45, EXP-46, EXP-48), the weather
#    split (EXP-48), the random-label null teacher (EXP-52, EXP-53) and the life alone read over
#    time from one taught brain (EXP-47)

WEATHER = {"kind": "weather_chain", "deadline": 10, "success_reward": 2.0, "failure_reward": -1.0}


def _searcher_by_enumeration(actions: int, stages: int, deadline: int) -> Fraction:
    """Every order in which the searcher can try the actions at every stage, equally likely."""
    wins = Fraction(0)
    orders = list(itertools.permutations(range(actions)))
    for choice in itertools.product(orders, repeat=stages):
        spent = sum(order.index(0) + 1 for order in choice)  # action 0 is the required one
        if spent <= deadline:
            wins += Fraction(1, len(orders) ** stages)
    return wins


def test_never_repeat_searcher_exact_value_of_exp45() -> None:
    assert me.never_repeat_chain_success_exact(5, 4, 10) == Fraction(190, 625)
    for actions, stages, deadline in ((3, 2, 3), (3, 3, 5), (4, 2, 4), (2, 4, 6)):
        assert me.never_repeat_chain_success_exact(actions, stages, deadline) == _searcher_by_enumeration(
            actions, stages, deadline)
    analytic = ru.analytic(COLD)
    assert analytic["never_repeat_searcher_success_fraction"] == "38/125"
    assert ru.analytic(WEATHER)["never_repeat_searcher_success"] == pytest.approx(0.304)


def test_searcher_control_never_repeats_a_failure_and_lands_on_the_exact_rate(monkeypatch) -> None:  # noqa: ANN001
    tried: list[tuple[int, int, int, bool]] = []
    original_step, original_make = wo.ColdChain.step, ru.make_world
    serial = itertools.count()

    def made(spec, cell=None):  # noqa: ANN001, ANN202
        world = original_make(spec, cell)
        world.serial = next(serial)  # one number per episode's world
        return world

    def logged(self, action):  # noqa: ANN001, ANN202
        before = self.stage
        outcome = original_step(self, action)
        tried.append((self.serial, before, int(action), outcome.advanced))
        return outcome

    monkeypatch.setattr(ru, "make_world", made)
    monkeypatch.setattr(wo.ColdChain, "step", logged)
    rows = ru.control_rows("searcher", COLD, episodes=400, seed=3)
    failures = [(w, s, a) for w, s, a, advanced in tried if not advanced]
    assert failures and len(failures) == len(set(failures)), "a failed action was tried again at the same stage"
    assert len({w for w, *_ in tried}) == 400
    monkeypatch.setattr(wo.ColdChain, "step", original_step)
    monkeypatch.setattr(ru, "make_world", original_make)
    rate = np.mean([r["success"] for r in ru.control_rows("searcher", COLD, episodes=20_000, seed=4)])
    assert abs(rate - 0.304) < 0.01
    assert all(r["decisions"] <= 10 for r in rows)
    with pytest.raises(ValueError):
        ru.control_rows("searcher", {"kind": "route_cue"}, episodes=1, seed=0, routes=[0])


def test_weather_chain_keeps_the_chain_rules_and_adds_only_the_weather() -> None:
    assert set(wo.WEATHER_SEEN).isdisjoint(wo.WEATHER_UNSEEN)
    assert all(sum(w) % 2 == 0 for w in wo.WEATHER_SEEN) and all(sum(w) % 2 == 1 for w in wo.WEATHER_UNSEEN)
    for bit in range(wo.WEATHER_BITS):  # every single bit value is taught; only combinations are new
        assert {w[bit] for w in wo.WEATHER_SEEN} == {0, 1}
    rng = np.random.default_rng(0)
    for _ in range(50):
        weather = wo.WEATHER_UNSEEN[int(rng.integers(4))]
        plain, dressed = wo.ColdChain(), wo.make_world(WEATHER, {"weather": list(weather)})
        assert dressed.inputs == 10
        while not plain.done:
            assert np.array_equal(dressed.observation()[:, :7], plain.observation())
            assert np.array_equal(dressed.observation()[0, 7:], np.asarray(weather, dtype=float))
            action = int(rng.integers(5))
            assert plain.step(action) == dressed.step(action)
        assert dressed.done
    situations = wo.chain_situations(WEATHER, {"weather": [1, 1, 1]})
    expected = [((0, 0, 0), wo.GATHER_WOOD), ((1, 0, 0), wo.GATHER_STONE), ((1, 1, 0), wo.CRAFT_FIRE),
                ((1, 1, 1), wo.WARM_UP)]
    for (stage, x, required), ((w, s, f), right) in zip(situations, expected):
        v5 = wo.v5_observation(wood=w, stone=s, fire=bool(f))  # EXP-45's obs(w, s, f), built directly
        assert np.array_equal(x, np.concatenate([v5, [[1.0, 1.0, 1.0]]], axis=1)) and required == right
    with pytest.raises(ValueError):
        wo.weather_cell([1, 2, 0])


def test_weather_schedules_teach_seen_and_test_unseen_and_never_move_shorter_lives() -> None:
    protocol = json.loads((HERE / "protocol-p3-generalization.json").read_text())
    train, after, evaluation = ru.schedules(protocol, 1001, 120)
    assert len(train) == 120 and after is None
    assert {tuple(c["weather"]) for c in train} == set(wo.WEATHER_SEEN)
    assert [tuple(c["weather"]) for c in evaluation[:8]] == list(wo.WEATHER_UNSEEN) * 2
    assert ru.schedules(protocol, 1001, 240)[0][:120] == train
    for world in ({"kind": "route_cue"}, {"kind": "recall"}):
        p = dict(protocol, world=world, withdrawal_episodes=10)
        assert ru.schedules(p, 7, 240)[0][:120] == ru.schedules(p, 7, 120)[0]
    assert ru.schedules(dict(protocol, world=COLD), 7, 120) == (None, None, None)


def test_random_label_teacher_speaks_at_the_correcting_moments_with_random_content() -> None:
    correct = _life(ad.StepAdapter(SpyBrain(seed=9), 5), ru.Caregiver("correct", 4, 8), episodes=60)
    null = _life(ad.StepAdapter(SpyBrain(seed=9), 5),
                 ru.Caregiver("random_label", 4, 8, rng=np.random.default_rng(1)), episodes=60)
    # the spy acts on its own stream, so both lives execute the same actions: the twin pairing
    assert [e["action"] for e in correct.events] == [e["action"] for e in null.events]
    assert [e["label"] is not None for e in correct.events] == [e["label"] is not None for e in null.events]
    labels = [e["label"] for e in null.events if e["label"] is not None]
    assert len(labels) > 100 and set(labels) == set(range(5))
    assert any(e["label"] != e["required"] for e in null.events if e["label"] is not None)
    again = _life(ad.StepAdapter(SpyBrain(seed=9), 5),
                  ru.Caregiver("random_label", 4, 8, rng=np.random.default_rng(1)), episodes=60)
    assert [e["label"] for e in again.events] == [e["label"] for e in null.events]
    with pytest.raises(ValueError):
        _life(ad.StepAdapter(SpyBrain(seed=9), 5), ru.Caregiver("random_label", 4, 8), episodes=5)


@pytest.mark.parametrize(
    "change, message",
    [
        ({"arms": {"x": {"adapter": "live", "caregiver": "random_label"}}}, "live takes no teacher"),
        ({"arms": {"x": {"adapter": "step", "caregiver": "none", "training_episodes": 0}}}, "at least one"),
        ({"arms": {"x": {"adapter": "step", "caregiver": "none", "twin_of": "y"},
                   "y": {"adapter": "step", "caregiver": "none"}}}, "earlier arm"),
        ({"arms": {"y": {"adapter": "step", "caregiver": "none"},
                   "x": {"adapter": "step", "caregiver": "grade", "twin_of": "y"}}}, "taught exactly"),
        ({"withdrawal_checkpoints": [10, 80]}, "strictly inside"),
        ({"withdrawal_checkpoints": [20, 10]}, "increasing"),
    ],
)
def test_protocol_refuses_ill_formed_copies(tmp_path: Path, change: dict, message: str) -> None:
    protocol = json.loads((HERE / "protocol-p1-drift.json").read_text())
    protocol.update(change)
    path = tmp_path / "protocol.json"
    path.write_text(json.dumps(protocol))
    with pytest.raises(ValueError, match=message):
        ru.load_protocol(path)


@needs_cadence
def test_per_state_reading_is_exp45s_reset_greedy_read_and_leaves_the_checkpoint(tmp_path: Path) -> None:
    from cadence import Brain

    from receipts import sha256_file

    brain = _small_brain(17)
    ru.run_life(ad.StepAdapter(brain, 5), COLD, ru.Caregiver("correct", 4, 8), 6, life_id="s")
    path = tmp_path / "trained.npz"
    brain.save(path)
    before = sha256_file(path)
    reading = ru.per_state(path, COLD, samples=20, seed=3)
    assert sha256_file(path) == before
    chain = reading["chain"]
    assert chain["situations"] == 4 and len(chain["stage_p_right"]) == 4
    reference = Brain.load(path)  # EXP-45's reading, written out
    answers = []
    for w, s, f in ((0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)):
        reference.reset()
        answers.append(int(reference.act(wo.v5_observation(wood=w, stone=s, fire=bool(f)), greedy=True)[0]))
    assert [r["greedy"] for r in chain["rows"]] == answers
    assert chain["accuracy"] == np.mean([a == r for a, r in zip(answers, range(4))])
    assert chain["memoryless_success"] == pytest.approx(me.chain_success(chain["stage_p_right"], 10))
    assert ru.per_state(path, COLD, samples=20, seed=3) == reading


@needs_cadence
@pytest.mark.parametrize("adapter_name", ["step", "live"])
def test_reading_the_life_alone_at_checkpoints_leaves_it_as_it_would_have_run(
        tmp_path: Path, adapter_name: str) -> None:
    from cadence import Brain

    import probes as pr

    brain = _small_brain(19)
    taught = ru.run_life(ad.StepAdapter(brain, 5), COLD, ru.Caregiver("correct", 4, 8), 4, life_id="t")
    path = tmp_path / "taught.npz"
    brain.save(path)
    seam = json.dumps(taught.seam.to_dict())
    one, two = Brain.load(path), Brain.load(path)
    whole = ru.run_withdrawal(ad.ADAPTERS[adapter_name](one, 5), COLD, 6, life_id="w",
                              seam=ad.PendingOutcome(**json.loads(seam)))
    marks: list[int] = []

    def at_mark(mark: int, held: ad.PendingOutcome) -> None:
        two.save(tmp_path / f"mark-{mark}.npz")
        ru.per_state(tmp_path / f"mark-{mark}.npz", COLD)
        marks.append(mark)

    stopped = ru.run_withdrawal(ad.ADAPTERS[adapter_name](two, 5), COLD, 6, life_id="w",
                                seam=ad.PendingOutcome(**json.loads(seam)), marks=[2, 4], at_mark=at_mark)
    assert marks == [2, 4] and stopped.counts["checkpoints"] == [2, 4]
    assert stopped.events == whole.events  # every action, outcome, choice and learning record
    assert [e["episode"] for e in stopped.episodes] == list(range(6))
    assert stopped.counts["outcomes_delivered"] == whole.counts["outcomes_delivered"]
    copier = pr.Copier(tmp_path / "c")
    assert pr.state_digest(one, copier) == pr.state_digest(two, copier)


@needs_cadence
def test_a_twin_continues_from_its_twins_taught_brain_and_every_reading_lands(tmp_path: Path) -> None:
    import report as rp

    protocol = json.loads((HERE / "protocol-p1-drift.json").read_text())
    protocol["recipes"] = {"small": {"compose": {"modules": [12], "arousal": True}}}
    protocol.update(training_episodes=3, withdrawal_episodes=3, withdrawal_checkpoints=[1, 2])
    protocol["evaluation"].update(episodes=4, per_state_samples=2)
    arms = ["correct_then_live", "correct_then_step"]
    result = ru.run_founder(protocol, 5, arms, "small", tmp_path)
    a, b = (result["arms"][arm] for arm in arms)
    assert b["taught_with"] == "correct_then_live" and "taught_with" not in a
    assert a["trained_digest"] == b["trained_digest"] and a["per_state"] == b["per_state"]
    assert not (tmp_path / "small" / "founder-5" / "correct_then_step-trained.npz").exists()
    for arm in (a, b):
        assert set(arm["withdrawal"]["checkpoints"]) == {"1", "2"}
        assert arm["withdrawal"]["counts"]["episodes"] == 3
        assert "chain" in arm["withdrawal"]["checkpoints"]["2"]["per_state"]
    assert {"founder", "random", "oracle", "searcher"} <= set(result["arms"])
    assert "per_state" in result["arms"]["founder"]
    bodies = [json.loads((tmp_path / "small" / "founder-5" / "founder.json").read_text())]
    assert rp.drift_table("small", bodies, protocol)[2].startswith("| arm | taught | after 1 | after 2 | after 3 |")
    assert any("correct_then_live-correct_then_step" in line for line in rp.pair_lines(bodies, protocol))
    assert rp.state_table("small", bodies, protocol)


@needs_cadence
def test_weather_founder_reads_seen_and_unseen_and_a_random_label_arm_runs(tmp_path: Path) -> None:
    import inspect

    from cadence import Brain

    protocol = json.loads((HERE / "protocol-p3-content.json").read_text())
    compose = {"modules": [12], "arousal": True}
    if "memory_choice" in inspect.signature(Brain.compose).parameters:  # the episodic memory, 0.83.0 on
        compose["memory_choice"] = True
    protocol["recipes"] = {"small": {"compose": compose}}
    protocol.update(withdrawal_episodes=2)
    protocol["evaluation"].update(episodes=4)
    for spec in protocol["arms"].values():
        spec["training_episodes"] = 3
    result = ru.run_founder(protocol, 6, ["correct_40", "random_label_40"], "small", tmp_path)
    reading = result["arms"]["random_label_40"]["withdrawal"]["per_state"]
    assert reading["seen"]["situations"] == reading["unseen"]["situations"] == 16
    assert reading["gap"] == reading["seen"]["accuracy"] - reading["unseen"]["accuracy"]
    teaching = result["arms"]["random_label_40"]["training"]["counts"]["teaching"]
    assert teaching["labels"] > 0
    assert result["arms"]["searcher"]["frozen"]["sampled"]["summary"]["episodes"] == 4


@needs_cadence
def test_reset_withdrawal_starts_from_the_brain_of_v5s_own_order(tmp_path: Path) -> None:
    """``withdrawal_reset``: the lesson's held outcome is delivered through the teaching
    interface with a fresh episode's observation, then ``Brain.reset``. The brain the life alone
    starts from equals the one of V5's loop as cadence-teachers' EXP-45 writes it out."""
    import probes as pr

    instrument = _small_brain(23)
    life = ru.run_life(ad.StepAdapter(instrument, 5), COLD, ru.Caregiver("correct", 4, 8), 5, life_id="i")
    ad.StepAdapter(instrument, 5).resume(life.seam, wo.ColdChain().observation())
    instrument.reset()

    v5 = _small_brain(23)
    world, decisions = wo.ColdChain(), 0
    action = int(v5.step(world.observation())[0])
    for _ in range(5):
        while True:
            guided = decisions % 12 < 4
            outcome = world.step(action)
            teacher = np.array([world.required()]) if guided and not outcome.advanced and not outcome.done else None
            decisions += 1
            if outcome.done:
                world = wo.ColdChain()
                action = int(v5.step(world.observation(), reward=np.array([outcome.reward]), done=np.array([True]))[0])
                break
            action = int(v5.step(world.observation(), reward=np.array([outcome.reward]), done=np.array([False]),
                                 teacher=teacher)[0])
    v5.reset()
    copier = pr.Copier(tmp_path / "c")
    assert pr.state_digest(instrument, copier) == pr.state_digest(v5, copier)


@needs_cadence
def test_a_reset_withdrawal_begins_afresh_and_the_flag_is_checked(tmp_path: Path) -> None:
    protocol = json.loads((HERE / "protocol-p1-drift.json").read_text())
    protocol["recipes"] = {"small": {"compose": {"modules": [12], "arousal": True}}}
    protocol.update(training_episodes=3, withdrawal_episodes=3, withdrawal_checkpoints=[1], withdrawal_reset=True)
    protocol["evaluation"].update(episodes=2, per_state_samples=0)
    result = ru.run_founder(protocol, 8, ["correct_then_live"], "small", tmp_path)
    counts = result["arms"]["correct_then_live"]["withdrawal"]["counts"]
    assert counts["resumed_learning"] is None and counts["episodes"] == 3 and counts["checkpoints"] == [1]
    protocol["withdrawal_reset"] = "yes"
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(protocol))
    with pytest.raises(ValueError, match="withdrawal_reset"):
        ru.load_protocol(path)


# -- the chain seen three ways, adapted from Will Glynn's cadence-teachers
#    (https://github.com/WGlynn/cadence-teachers): the ambiguous chain Huncho reported on the Stone
#    Age world as EXP-56 and EXP-57 rebuilt it (progress hidden), EXP-59's invisible step and
#    EXP-60's visible chain. The arrays below are the notebook's own literals.

EXP56_OBS_A = np.array([[0.35, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])  # stages 1 and 3 of EXP-56
EXP56_OBS_B = np.array([[0.35, 1.0, 0.0, 0.0, 0.5, 0.0, 1.0]])  # stages 2 and 4 of EXP-56
EXP59_OBS_C = np.array([[0.35, 1.0, 1.0, 0.0, 0.5, 0.5, 1.0]])  # stage 4 of EXP-59
EXP60_STAGES = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]  # (wood, stone, fire), EXP-45's obs()


def _exp60_visible(stage: int) -> np.ndarray:
    w, s, f = EXP60_STAGES[stage]
    return np.array([[0.35, float(w), float(s), float(f), w / 2.0, s / 2.0, 1.0]])


def _views_along_the_chain(view: str) -> list[np.ndarray]:
    world = wo.make_world({"kind": "view_chain", "view": view})
    seen = []
    while not world.done:
        seen.append(world.observation())
        world.step(world.required())
    return seen


def test_view_chains_show_the_notebooks_observations_byte_for_byte() -> None:
    hidden = _views_along_the_chain("hidden")
    assert [x.tobytes() for x in hidden] == [x.tobytes() for x in
                                             (EXP56_OBS_A, EXP56_OBS_B, EXP56_OBS_A, EXP56_OBS_B)]
    assert hidden[0].tobytes() == hidden[2].tobytes() and hidden[1].tobytes() == hidden[3].tobytes()
    assert hidden[0].tobytes() != hidden[1].tobytes()
    invisible = _views_along_the_chain("invisible")
    assert [x.tobytes() for x in invisible] == [x.tobytes() for x in
                                                (EXP56_OBS_A, EXP56_OBS_A, EXP56_OBS_B, EXP59_OBS_C)]
    visible = _views_along_the_chain("visible")
    cold = wo.ColdChain()
    for stage, x in enumerate(visible):
        assert x.tobytes() == _exp60_visible(stage).tobytes() == cold.observation().tobytes(), stage
        cold.step(cold.required())
    for x in hidden + invisible + visible:
        assert x.dtype == np.float64 and x.shape == (1, wo.V5_INPUTS)
    assert not wo.views_distinct({"kind": "view_chain", "view": "hidden"})
    assert not wo.views_distinct({"kind": "view_chain", "view": "invisible"})
    assert wo.views_distinct({"kind": "view_chain", "view": "visible"}) and wo.views_distinct(COLD)


@pytest.mark.parametrize("view", sorted(wo.CHAIN_VIEWS))
def test_view_chains_keep_v5s_rules_and_pay(view: str) -> None:
    rng = np.random.default_rng(202)
    for _ in range(300):
        plain = wo.ColdChain()
        seen = wo.make_world({"kind": "view_chain", "view": view, "deadline": 10,
                              "success_reward": 2.0, "failure_reward": -1.0})
        while not plain.done:
            before = seen.observation()
            action = int(rng.integers(5))
            right = action == plain.required()
            outcome = seen.step(action)
            assert plain.step(action) == outcome  # stage, required action, reward, reason
            if not right and not outcome.done:  # a wrong action changes nothing the brain sees
                assert seen.observation().tobytes() == before.tobytes()
        assert seen.done and seen.success == plain.success and seen.decisions == plain.decisions
    with pytest.raises(ValueError):
        wo.make_world({"kind": "view_chain", "view": "foggy"})


def test_the_invisible_steps_right_action_changes_nothing_seen() -> None:
    world = wo.make_world({"kind": "view_chain", "view": "invisible"})
    before = world.observation()
    outcome = world.step(wo.GATHER_WOOD)
    assert outcome.advanced and world.stage == 1 and world.observation().tobytes() == before.tobytes()
    assert world.required() == wo.GATHER_STONE
    hidden = wo.make_world({"kind": "view_chain", "view": "hidden"})
    hidden.step(wo.GATHER_WOOD)
    assert hidden.observation().tobytes() != before.tobytes()  # on the hidden view it does


@pytest.mark.parametrize("view", sorted(wo.CHAIN_VIEWS))
def test_view_chain_scorer_controls_and_analytic_values(view: str) -> None:
    spec = {"kind": "view_chain", "view": view, "deadline": 10, "success_reward": 2.0,
            "failure_reward": -1.0}
    analytic = ru.analytic(spec)
    assert analytic["uniform_random_success_fraction"] == ru.analytic(COLD)["uniform_random_success_fraction"]
    if view == "visible":
        assert analytic["never_repeat_searcher_success_fraction"] == "38/125"
    else:
        assert "never_repeat_searcher_success" not in analytic and "measured" in analytic["note"]
    rows = ru.control_rows("oracle", spec, episodes=10, seed=0)
    assert all(r["success"] and r["decisions"] == 4 for r in rows)
    rate = np.mean([r["success"] for r in ru.control_rows("random", spec, episodes=20_000, seed=2)])
    assert abs(rate - 0.1208738816) < 0.01
    searched = ru.control_rows("searcher", spec, episodes=200, seed=3)
    assert len(searched) == 200 and all(r["decisions"] <= 10 for r in searched)


# -- context rules: which decisions enter the episodic memory's temporal context key. The hold
#    rule and the in-sequence reading are Will Glynn's, cadence-teachers EXP-56 and EXP-57
#    (https://github.com/WGlynn/cadence-teachers, exp/EXP-56_ambiguous_chain_trace.py).

import context_rules as cr  # noqa: E402

HIDDEN = {"kind": "view_chain", "view": "hidden", "deadline": 10, "success_reward": 2.0, "failure_reward": -1.0}


def test_exact_mcnemar_reproduces_exp56_and_exp57() -> None:
    assert me.mcnemar_exact(14, 2) == pytest.approx(0.0042, abs=1e-4)  # EXP-56, p = .004
    assert me.mcnemar_exact(9, 2) == pytest.approx(0.0654, abs=1e-4)  # EXP-57, natural
    assert me.mcnemar_exact(19, 5) == pytest.approx(0.0066, abs=1e-4)  # EXP-57, 240 pooled
    assert me.mcnemar_exact(8, 4) == pytest.approx(0.3877, abs=1e-4)
    assert me.mcnemar_exact(36, 2) < 1e-4 and me.mcnemar_exact(2, 36) == me.mcnemar_exact(36, 2)
    assert me.mcnemar_exact(0, 0) == 1.0 and me.mcnemar_exact(3, 3) == 1.0
    with pytest.raises(ValueError):
        me.mcnemar_exact(-1, 2)


def test_in_sequence_summary_counts_first_tries_and_retries() -> None:
    episodes = [
        {"success": True, "decisions": 4, "stage_reached": 4, "reason": "success",
         "first_try": [1, 1, 1, 1], "retries": 0, "retries_right": 0},
        {"success": False, "decisions": 10, "stage_reached": 1, "reason": "timeout",
         "first_try": [0, 0, None, None], "retries": 8, "retries_right": 1},
    ]
    summary = me.episode_summary(episodes, 4)
    assert summary["first_try_accuracy"] == [0.5, 0.5, 1.0, 1.0]
    assert summary["first_try_reached"] == [2, 2, 1, 1]
    assert summary["retries"] == 8 and summary["retry_accuracy"] == 1 / 8
    assert summary["exact_minimal_completions"] == 1


class _Critic:
    def __init__(self) -> None:
        self.config = type("Config", (), {"gamma": 0.9})()
        self.critic_index = np.array([0])
        self.w_critic = np.array([1.0])
        self.b_critic = 0.0
        self.state = None

    def value(self, state):  # noqa: ANN001, ANN202
        return state.activation[:, self.critic_index] @ self.w_critic + self.b_critic


class _State:
    def __init__(self, value: float) -> None:
        self.activation = np.array([[value]])


class _ContextSpy:
    """Only what a rule touches: ``_context``, the critic, ``learn`` and ``_choose``. Each
    decision adds its observation and action to the context; ``learn`` settles the next
    state at a scripted value and clears the context at the end of an attempt."""

    def __init__(self) -> None:
        self._context = None
        self.basal_ganglia = _Critic()
        self.keys: list[np.ndarray | None] = []
        self.next_value = 0.0

    def _choose(self, x, drive, free, *, greedy, temperature=None):  # noqa: ANN001, ANN202
        self.keys.append(None if self._context is None else self._context.copy())
        self._context = (np.zeros(2) if self._context is None else self._context * 0.5) + np.asarray(x).reshape(-1)[:2]
        return np.array([0])

    def learn(self, reward, done, next_observations, **options):  # noqa: ANN001, ANN202
        self.basal_ganglia.state = _State(self.next_value)
        if bool(np.asarray(done)[0]):
            self._context = np.zeros(2)
        return {"value": self.value_now, "td_error": 0.0, "dopamine": 0.0}


def test_context_rule_arithmetic_on_a_spy() -> None:
    a, b = np.array([[1.0, 0.0]]), np.array([[0.0, 1.0]])
    for name, judgments in (("hold", [True, True]), ("hold_td", [False, True])):
        spy = _ContextSpy()
        rule = cr.ContextRule(spy, name)
        spy.value_now = 1.0
        rule.choose(a, None, _State(1.0), greedy=True)
        first = spy._context.copy()
        # the outcome: the observation unchanged; the critic's error 0 + 0.9 * 2.0 - 1.0 > 0
        spy.next_value = 2.0
        spy.learn(np.array([0.0]), np.array([False]), a)
        assert rule.last["unchanged"] and rule.last["held"] == judgments[0]
        assert rule.last["error"] == (None if name == "hold" else pytest.approx(0.8))
        rule.choose(a, None, _State(2.0), greedy=True)
        assert (spy.keys[-1] is None) == judgments[0]  # held: the key is the first decision's
        if not judgments[0]:
            assert np.array_equal(spy.keys[-1], first)
        # again unchanged; now the error 0 + 0.9 * 1.0 - 2.0 < 0
        spy.value_now, spy.next_value = 2.0, 1.0
        spy.learn(np.array([0.0]), np.array([False]), a)
        assert rule.last["held"] == judgments[1]
        # a changed observation is never held
        rule.choose(a, None, _State(1.0), greedy=True)
        spy.value_now, spy.next_value = 1.0, 0.0
        spy.learn(np.array([0.0]), np.array([False]), b)
        assert not rule.last["unchanged"] and not rule.last["held"]
        # never across the end of an attempt: the cleared context stays cleared
        rule.choose(b, None, _State(1.0), greedy=True)
        spy.learn(np.array([-1.0]), np.array([True]), b)
        assert not rule.last["held"] and np.array_equal(spy._context, np.zeros(2))
        assert rule.counts()["rule"] == name and rule.counts()["held"] == sum(judgments)
    # a frozen reading: no learn, the error is gamma V(next) - V(chosen), with a zero reward
    spy = _ContextSpy()
    rule = cr.ContextRule(spy, "hold_td")
    rule.choose(a, None, _State(1.0), greedy=True)
    rule.choose(a, None, _State(1.0), greedy=True)
    assert rule.last["error"] == pytest.approx(-0.1) and rule.last["held"]
    rule.choose(a, None, _State(2.0), greedy=True)
    assert rule.last["error"] == pytest.approx(0.8) and not rule.last["held"]
    untouched = _ContextSpy()
    assert cr.ContextRule(untouched, "none").rule == "none" and "learn" not in vars(untouched)
    second = cr.ContextRule(untouched, "hold")
    third = cr.ContextRule(untouched, "hold_td")  # replaces the second, never wraps it
    assert untouched.learn.__self__ is third and third._learn.__self__ is untouched
    cr.ContextRule(untouched, "none")
    assert "learn" not in vars(untouched) and "_choose" not in vars(untouched) and second.rule == "hold"
    with pytest.raises(ValueError):
        cr.ContextRule(_ContextSpy(), "forget")


def _memory_brain(seed: int = 29, context: float = 0.5):  # noqa: ANN202
    from cadence import Brain

    return Brain.compose(inputs=7, actions=5, modules=(12,), seed=seed, arousal=True, memory_choice=True,
                         memory_context=context)


@needs_cadence
def test_hold_keeps_a_retrys_key_equal_to_the_first_try() -> None:
    """EXP-56's mechanical check: with hold, a retry's decision key equals the first try's;
    without, it differs; without a context store the rule has nothing to hold."""
    x = wo.VIEW_A
    for rule, same in (("none", False), ("hold", True), ("hold_td", None)):
        brain = _memory_brain()
        cr.ContextRule(brain, rule)
        keys = []
        for _ in range(3):
            brain.act(x, greedy=True)
            keys.append(brain._decision.copy())
        if same is not None:
            assert all(np.array_equal(keys[0], k) for k in keys[1:]) == same
    place = _memory_brain(context=0.0)
    rule = cr.ContextRule(place, "hold")
    for _ in range(3):
        place.act(x, greedy=True)
    assert place.context_memory is None and rule.held == 0 and rule.unchanged == 0


class _Exp56Trace:
    """Will Glynn's ``Trace`` from cadence-teachers, exp/EXP-56_ambiguous_chain_trace.py, as
    written there: with hold, a decision whose next observation is unchanged never enters the
    stream's temporal context; never across a boundary."""

    def __init__(self, brain, hold: bool) -> None:  # noqa: ANN001
        self.b, self.hold = brain, hold
        self.prev, self.pre = None, None

    def call(self, fn, x, boundary=False, **kw):  # noqa: ANN001, ANN202
        b = self.b
        if self.hold and not boundary and self.prev is not None and np.array_equal(x, self.prev):
            b._context = None if self.pre is None else self.pre.copy()
        if boundary:
            pre = None if b._context is None else np.zeros_like(b._context)
        else:
            pre = None if b._context is None else b._context.copy()
        out = fn(x, **kw)
        self.prev, self.pre = x.copy(), pre
        return int(np.asarray(out).reshape(-1)[0])


@needs_cadence
@pytest.mark.parametrize("view", ["hidden", "invisible"])
def test_the_hold_rule_lives_exactly_as_the_notebooks_trace(tmp_path: Path, view: str) -> None:
    import probes as pr

    spec = dict(HIDDEN, view=view)
    instrument = _memory_brain(31)
    life = ru.run_life(ad.StepAdapter(instrument, 5, context_rule="hold"), spec, ru.Caregiver("correct", 4, 8), 6,
                       life_id="h")
    ad.StepAdapter(instrument, 5, context_rule="hold").resume(life.seam, wo.make_world(spec).observation())
    instrument.reset()

    notebook = _memory_brain(31)  # EXP-56's train(), corrective signal
    trace = _Exp56Trace(notebook, hold=True)
    world, g, actions = wo.make_world(spec), 0, []
    a = trace.call(notebook.step, world.observation())
    for _ in range(6):
        while True:
            guided = (g % 12) < 4
            right = world.required()
            outcome = world.step(a)
            actions.append(a)
            teacher = np.array([right]) if (guided and not outcome.advanced and not world.done) else None
            g += 1
            if world.done:
                world = wo.make_world(spec)
                a = trace.call(notebook.step, world.observation(), boundary=True,
                               reward=np.array([outcome.reward]), done=np.array([True]))
                break
            kw = {"reward": np.array([outcome.reward]), "done": np.array([False])}
            if teacher is not None:
                kw["teacher"] = teacher
            a = trace.call(notebook.step, world.observation(), **kw)
    notebook.reset()
    assert [e["action"] for e in life.events] == actions
    assert life.counts["context_rule"]["held"] > 0
    copier = pr.Copier(tmp_path / "c")
    assert pr.state_digest(instrument, copier) == pr.state_digest(notebook, copier)


@needs_cadence
def test_the_failure_rule_judges_with_learns_own_td_error() -> None:
    brain = _memory_brain(37)
    life = ru.run_life(ad.StepAdapter(brain, 5, context_rule="hold_td"), HIDDEN, ru.Caregiver("none", 0, 1), 8,
                       life_id="td")
    judged = 0
    for event, following in zip(life.events, life.events[1:]):
        judgment = following["choice"].get("context_rule", {})
        if judgment.get("error") is None:
            continue
        judged += 1
        learning = event["learning"]
        assert abs(judgment["error"]) == pytest.approx(learning["td_error"], rel=1e-9, abs=1e-12)
        assert np.sign(judgment["error"]) == np.sign(learning["dopamine"])
        if judgment["held"]:
            assert judgment["unchanged"] and judgment["error"] < 0
    assert judged > 20 and life.counts["context_rule"]["unchanged"] >= life.counts["context_rule"]["held"]


@needs_cadence
def test_a_reading_under_a_rule_is_seeded_isolated_and_counts_the_rule(tmp_path: Path) -> None:
    import probes as pr

    brain = _memory_brain(41)
    ru.run_life(ad.StepAdapter(brain, 5, context_rule="hold"), HIDDEN, ru.Caregiver("correct", 4, 8), 4,
                life_id="r")
    path = tmp_path / "trained.npz"
    brain.save(path)
    copier = pr.Copier(tmp_path / "c")
    before = pr.state_digest(brain, copier)
    rows = ru.evaluate(path, HIDDEN, episodes=8, greedy=False, seed=5, context_rule="hold")
    assert rows == ru.evaluate(path, HIDDEN, episodes=8, greedy=False, seed=5, context_rule="hold")
    assert pr.state_digest(brain, copier) == before
    for row in rows:
        assert len(row["first_try"]) == 4 and row["rule_held"] <= row["rule_unchanged"]
        assert row["retries"] == row["decisions"] - sum(v is not None for v in row["first_try"])
        # on the hidden view the observation stays the same exactly after a miss; the episode's
        # last decision is judged by no later one
        misses = row["decisions"] - row["stage_reached"]
        assert row["rule_unchanged"] in (misses, misses - 1)
        if row["success"]:
            assert row["rule_unchanged"] == misses == row["rule_held"]
    plain = ru.evaluate(path, HIDDEN, episodes=2, greedy=True, seed=5)
    assert "rule_held" not in plain[0] and plain[0]["first_try"][0] in (0, 1)


@needs_cadence
def test_a_founder_on_the_hidden_view_reads_every_rule_and_pairs_clean_passes(tmp_path: Path) -> None:
    protocol = json.loads((HERE / "protocol-keys-hidden.json").read_text())
    protocol["recipes"] = {"small": {"compose": {"modules": [12], "arousal": True, "memory_choice": True}}}
    protocol["evaluation"].update(episodes=3)
    arms = ["place_natural_120", "ctx5_natural_120", "hold5_natural_120", "holdtd_natural_120"]
    for arm in arms:
        protocol["arms"][arm]["training_episodes"] = 3
    result = ru.run_founder(protocol, 3, arms, "small", tmp_path)
    for arm in arms:
        reading = result["arms"][arm]["frozen"]
        assert reading["greedy"]["summary"]["episodes"] == 1 and reading["sampled"]["summary"]["episodes"] == 3
        assert len(reading["sampled"]["summary"]["first_try_accuracy"]) == 4
        assert "per_state" not in result["arms"][arm]  # a hidden view has no stage-alone reading
    counts = {arm: result["arms"][arm]["training"]["counts"].get("context_rule") for arm in arms}
    assert counts["ctx5_natural_120"] is None and counts["hold5_natural_120"]["rule"] == "hold"
    assert counts["holdtd_natural_120"]["rule"] == "hold_td"
    assert "rule_held" in result["arms"]["hold5_natural_120"]["frozen"]["sampled"]["summary"]
    assert result["arms"]["founder"].get("per_state") is None
    pairs = ru.pair_contrasts([result], dict(protocol, analysis={"pairs": [["hold5_natural_120", "ctx5_natural_120"]]}))
    clean = pairs["clean:trained:hold5_natural_120-ctx5_natural_120"]
    assert clean["founders"] == 1 and 0.0 <= clean["mcnemar_p"] <= 1.0
    assert "first_try_1:trained:hold5_natural_120-ctx5_natural_120" in pairs
    bad = dict(protocol, arms={"x": {"adapter": "step", "caregiver": "none", "context_rule": "forget"}})
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(bad))
    with pytest.raises(ValueError, match="context rule"):
        ru.load_protocol(path)
