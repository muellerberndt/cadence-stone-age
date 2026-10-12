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
