"""The ordered recall world: two written values, then a query for the first or the latest."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import worlds  # noqa: E402


def test_the_first_query_asks_for_the_older_write_under_its_own_marker() -> None:
    for condition in worlds.ORDER_CONDITIONS:
        for value in (0, 1):
            world = worlds.make_world({"kind": "recall", "ask": "order"},
                                      {"condition": condition, "value": value, "seed": 3})
            assert world.inputs == worlds.RECALL_INPUTS + 1
            events = world.events
            writes = [x for x in events if x[0, worlds.RECALL_WRITE] == 1.0]
            assert len(writes) == 2
            first = condition.startswith("ask-first")
            asked = writes[0] if first else writes[1]
            np.testing.assert_array_equal(asked[0, worlds.RECALL_PAYLOAD], worlds.RECALL_TOKENS[value])
            query = events[-1]
            assert query[0, worlds.RECALL_QUERY_FIRST] == (1.0 if first else 0.0)
            assert query[0, worlds.RECALL_QUERY] == (0.0 if first else 1.0)
            assert (len(events) == 6) == condition.endswith("-gap")


def test_the_plain_recall_world_is_unchanged() -> None:
    world = worlds.make_world({"kind": "recall"}, {"condition": "order-latest", "value": 1, "seed": 0})
    assert world.inputs == worlds.RECALL_INPUTS == 9
    assert all(x.shape == (1, 9) for x in world.events)


def test_the_efference_view_shows_the_last_executed_action() -> None:
    plain = worlds.make_world({"kind": "view_chain", "view": "invisible"})
    world = worlds.make_world({"kind": "view_chain", "view": "invisible", "efference": True})
    assert world.inputs == plain.inputs + world.actions
    first = world.observation()
    np.testing.assert_array_equal(first[0, :plain.inputs], plain.observation()[0])
    assert not first[0, plain.inputs:].any()
    world.step(3)
    seen = world.observation()
    assert seen[0, plain.inputs + 3] == 1.0 and seen[0, plain.inputs:].sum() == 1.0


def test_a_numbered_gap_puts_that_many_neutral_events_between_the_writes() -> None:
    for k in (4, 16, 48):
        world = worlds.make_world({"kind": "recall", "ask": "order"},
                                  {"condition": f"ask-first-gap{k}", "value": 1, "seed": 0})
        events = world.events
        writes = [i for i, x in enumerate(events) if x[0, worlds.RECALL_WRITE] == 1.0]
        assert writes[1] - writes[0] == k + 1
        assert events[-1][0, worlds.RECALL_QUERY_FIRST] == 1.0
