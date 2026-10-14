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
