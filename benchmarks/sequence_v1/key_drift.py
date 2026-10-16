"""Key drift of the episodic memory keyed on the cortex (protocol-cortex-keys-key-drift.json).

    python key_drift.py --protocol protocol-cortex-keys-key-drift.json --out OUT \
        [--seeds 1001 ...] [--recipes cortex sensory] [--arms correct_then_live ...] [--check]

Lives the drift design's life (V5's COLD chain, taught through ``step``, then alone through
``live``) on the instrument's adapters and caregiver. Every place-record write outside replay
is kept with the drive and the warm state of the settle its key came from. At each declared
reading point, between two episodes, every kept write is keyed again: the same drive settled
from the same warm state with the present graph. The reading compares the place separator's
codes of the old and the new key and reads the place records under both. Readings use the
brain's qualified settle and its stores' reads only, and restore the settlement report, so the
life goes on exactly as it would without them (``--check`` verifies this on one founder).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import runner  # noqa: E402
from adapters import ADAPTERS  # noqa: E402
from probes import Copier, state_digest  # noqa: E402
from worlds import chain_situations, make_world  # noqa: E402


def digest(x: np.ndarray) -> bytes:
    return np.ascontiguousarray(x, dtype=np.float64).tobytes()


class Keeper:
    """Keeps every place-record write outside replay with the settle its key came from."""

    def __init__(self, brain: Any, required: dict[bytes, int], cortex: bool) -> None:
        from cadence.patch import _copy_state  # noqa: PLC0415

        self.brain = brain
        self.required = required
        self.cortex = cortex
        self.episode = 0
        self.writes: list[dict[str, Any]] = []
        self.unmatched = 0
        self._settles: OrderedDict[int, tuple[Any, np.ndarray, np.ndarray, Any]] = OrderedDict()
        self._last: dict[str, Any] | None = None
        self._replaying = False
        settled, choose = brain._settled, brain._choose
        remember, replay = brain._remember, brain._replay

        def keep_settled(x: np.ndarray) -> tuple[np.ndarray, Any]:
            warm = _copy_state(brain._activity())
            drive, state = settled(x)
            self._settles[id(state)] = (state, np.array(x, copy=True), drive.copy(), warm)
            while len(self._settles) > 8:
                self._settles.popitem(last=False)
            return drive, state

        def keep_choose(x: np.ndarray, drive: np.ndarray, free: Any, **options: Any) -> Any:
            entry = self._settles.get(id(free))
            if entry is not None and entry[0] is free:
                self._last = {"x": entry[1], "drive": entry[2], "warm": entry[3],
                              "place": np.array(brain._place_key(x, free), copy=True)}
            else:
                self._last = None
            return choose(x, drive, free, **options)

        def keep_remember(places: np.ndarray, keys: Any, action: np.ndarray, value: np.ndarray,
                          streams: np.ndarray, salience: Any = None) -> None:
            if not self._replaying:
                self._keep(places, action, value, streams)
            remember(places, keys, action, value, streams, salience)

        def keep_replay(*args: Any, **kwargs: Any) -> None:
            self._replaying = True
            try:
                replay(*args, **kwargs)
            finally:
                self._replaying = False

        brain._settled, brain._choose = keep_settled, keep_choose
        brain._remember, brain._replay = keep_remember, keep_replay

    def _source(self, place: np.ndarray) -> dict[str, Any] | None:
        """The settle a written key came from: the last decision's, or a recent settle's (a
        demonstration is keyed by the settle of the act that follows its lesson)."""
        if self._last is not None and np.array_equal(self._last["place"], place):
            return self._last
        for state, x, drive, warm in reversed(self._settles.values()):
            if np.array_equal(self.brain._place_key(x, state), place):
                return {"x": x, "drive": drive, "warm": warm, "place": place}
        return None

    def _keep(self, places: np.ndarray, action: np.ndarray, value: np.ndarray,
              streams: np.ndarray) -> None:
        for row in np.flatnonzero(streams):
            place = np.array(places[row : row + 1], copy=True)
            if not self.cortex:  # the founder key is the observation; it is never keyed again
                source: dict[str, Any] | None = {"x": place, "drive": None, "warm": None}
            else:
                source = self._source(place)
            if source is None:
                self.unmatched += 1
                continue
            x = source["x"][row : row + 1] if self.cortex else place
            self.writes.append({
                "episode": self.episode,
                "x": x,
                "required": self.required.get(digest(x[0])),
                "action": int(np.asarray(action)[row]),
                "value": float(value[row]),
                "old": place,
                "drive": None if source["drive"] is None else source["drive"][row : row + 1],
                "warm": source["warm"],
            })


def read(brain: Any, keeper: Keeper, point: int, cortex: bool) -> list[dict[str, Any]]:
    """Every kept write keyed again with the present graph; nothing the life uses changes."""
    report = brain._last_settlement
    memory = brain.hippocampus
    separator = memory.separator
    rows = []
    try:
        for write in keeper.writes:
            old = write["old"]
            row: dict[str, Any] = {"point": point, "written": write["episode"],
                                   "age": point - write["episode"], "value": write["value"],
                                   "required": write["required"]}
            if cortex:
                try:
                    state = brain._qualified(write["drive"], write["warm"], operation="act")
                except RuntimeError:
                    row["refused"] = True
                    rows.append(row)
                    continue
                new = np.array(brain._place_key(write["x"], state), copy=True)
                codes = separator.code(np.vstack([old, new]))
                winners = [set(np.flatnonzero(code)) for code in codes]
                units = memory._delta_unit(codes)
                row["overlap"] = len(winners[0] & winners[1]) / separator.winners
                row["cosine"] = float(units[0] @ units[1])
                keys = {"old": old, "new": new}
            else:
                keys = {"old": old}
            reads = {name: np.asarray(memory.recall(key))[0] for name, key in keys.items()}
            for name, values in reads.items():
                required = write["required"]
                if required is not None:
                    others = np.delete(values, required)
                    row[f"accurate_{name}"] = bool(values[required] > others.max())
            if "new" in reads:
                row["agree"] = bool(np.argmax(reads["old"]) == np.argmax(reads["new"]))
            rows.append(row)
    finally:
        brain._last_settlement = report
    return rows


def live_arm(protocol: dict[str, Any], seed: int, recipe: str, arm: str, readings: bool) -> dict:
    world = protocol["world"]
    spec = protocol["arms"][arm]
    brain = runner.compose(protocol["recipes"][recipe], seed, world, {})
    cortex = getattr(brain, "memory_key", "sensory") == "cortex"
    required = {digest(x): req for _, x, req in chain_situations(world, None)}
    keeper = Keeper(brain, required, cortex)
    points = [int(p) for p in protocol["readings"]["points"]]
    rows: list[dict[str, Any]] = []
    calls = {"episodes": 0}
    original = runner.make_world

    def episode_world(spec_: dict[str, Any], route: Any = None) -> Any:
        index = calls["episodes"]
        keeper.episode = index
        if readings and index in points and index not in (0, training):
            rows.extend(read(brain, keeper, index, cortex))
        calls["episodes"] += 1
        return original(spec_, route)

    training = int(protocol["training_episodes"])
    alone = int(protocol["withdrawal_episodes"])
    actions = make_world(world, route=0).actions
    schedule = protocol["schedule"]
    runner.make_world = episode_world
    try:
        adapter = ADAPTERS[spec["adapter"]](brain, actions)
        caregiver = runner.Caregiver(spec["caregiver"], schedule["guided"], schedule["autonomous"])
        life = runner.run_life(adapter, world, caregiver, training,
                               life_id=f"{recipe}/{seed}/{arm}/train")
        if readings and training in points:
            rows.extend(read(brain, keeper, training, cortex))
        follow = ADAPTERS[spec["withdrawal_adapter"]](brain, actions)
        after = runner.run_withdrawal(follow, world, alone, life_id=f"{recipe}/{seed}/{arm}/alone",
                                      seam=life.seam)
        if readings and training + alone in points:
            keeper.episode = training + alone
            rows.extend(read(brain, keeper, training + alone, cortex))
    finally:
        runner.make_world = original
    copier = Copier()
    try:
        final = state_digest(brain, copier)
    finally:
        copier.close()
    return {"seed": seed, "recipe": recipe, "arm": arm, "readings": readings,
            "writes": len(keeper.writes), "unmatched": keeper.unmatched,
            "taught_success": float(np.mean([e["success"] for e in life.episodes])),
            "alone_success": float(np.mean([e["success"] for e in after.episodes])),
            "final_digest": final, "rows": rows}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="*")
    parser.add_argument("--recipes", nargs="*")
    parser.add_argument("--arms", nargs="*")
    parser.add_argument("--check", action="store_true",
                        help="the declared check: one life with and without the readings")
    args = parser.parse_args(argv)
    protocol = json.loads(args.protocol.read_text())
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / "protocol.json").write_bytes(args.protocol.read_bytes())
    started = time.time()
    if args.check:
        seed, recipe, arm = protocol["seeds"]["development"][0], "cortex", "correct_then_live"
        with_readings = live_arm(protocol, seed, recipe, arm, True)
        without = live_arm(protocol, seed, recipe, arm, False)
        check = {"seed": seed, "recipe": recipe, "arm": arm,
                 "with_readings": with_readings["final_digest"],
                 "without_readings": without["final_digest"],
                 "same": with_readings["final_digest"] == without["final_digest"]}
        (args.out / "check.json").write_text(json.dumps(check, indent=1))
        print(json.dumps(check))
        return 0 if check["same"] else 1
    seeds = args.seeds or protocol["seeds"]["development"]
    recipes = args.recipes or list(protocol["recipes"])
    arms = args.arms or list(protocol["arms"])
    for recipe in recipes:
        for seed in seeds:
            for arm in arms:
                result = live_arm(protocol, seed, recipe, arm, True)
                path = args.out / f"{recipe}-{seed}-{arm}.json"
                path.write_text(json.dumps(result))
                print(json.dumps({k: result[k] for k in ("seed", "recipe", "arm", "writes", "unmatched",
                                                          "taught_success", "alone_success")}),
                      flush=True)
    (args.out / "wall.json").write_text(json.dumps({"seconds": time.time() - started}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
