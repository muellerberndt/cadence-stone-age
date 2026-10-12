"""Exact chain probabilities, episode summaries and founder-level paired statistics.

The independent unit is the founder: episodes of one acquired brain are correlated, so
intervals resample founders, never pooled episodes.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Sequence
from fractions import Fraction
from typing import Any

import numpy as np


def chain_success(advance: Sequence[float], deadline: int) -> float:
    """Probability that a memoryless policy completes every stage within ``deadline``
    decisions, when stage ``s`` advances with probability ``advance[s]`` per decision and a
    failed decision leaves the stage unchanged (V5's no-op rule)."""
    if deadline < 0 or any(not 0.0 <= p <= 1.0 for p in advance):
        raise ValueError("deadline is nonnegative and probabilities lie in [0, 1]")
    stages = len(advance)
    # mass[s] = probability of being at stage s with the current decisions spent
    mass = np.zeros(stages + 1)
    mass[0] = 1.0
    for _ in range(deadline):
        following = np.zeros_like(mass)
        following[stages] = mass[stages]
        for s in range(stages):
            following[s + 1] += mass[s] * advance[s]
            following[s] += mass[s] * (1.0 - advance[s])
        mass = following
    return float(mass[stages])


def uniform_chain_success_exact(actions: int, stages: int, deadline: int) -> Fraction:
    """Uniform random's exact rational success: P[Binomial(deadline, 1/actions) >= stages]."""
    p = Fraction(1, actions)
    return sum(
        (
            Fraction(math.comb(deadline, k)) * p**k * (1 - p) ** (deadline - k)
            for k in range(stages, deadline + 1)
        ),
        Fraction(0),
    )


def first_passage(advance: Sequence[float], deadline: int) -> list[float]:
    """Probability that the chain completes exactly at decision ``t`` (index t-1)."""
    stages = len(advance)
    mass = np.zeros(stages + 1)
    mass[0] = 1.0
    out = []
    for _ in range(deadline):
        following = np.zeros_like(mass)
        for s in range(stages):
            following[s + 1] += mass[s] * advance[s]
            following[s] += mass[s] * (1.0 - advance[s])
        out.append(float(following[stages]))
        following[stages] = 0.0  # absorbed: count each completion once
        mass = following
    return out


def episode_summary(episodes: Sequence[dict[str, Any]], stages: int) -> dict[str, Any]:
    """Success, completion within the deadline, exact four-choice completion, stage reach."""
    n = len(episodes)
    if n == 0:
        return {"episodes": 0}
    success = [bool(e["success"]) for e in episodes]
    decisions = [int(e["decisions"]) for e in episodes]
    reach = Counter(int(e["stage_reached"]) for e in episodes)
    exact = sum(1 for s, d in zip(success, decisions) if s and d == stages)
    return {
        "episodes": n,
        "successes": int(sum(success)),
        "success_rate": sum(success) / n,
        "exact_minimal_completions": exact,
        "exact_minimal_rate": exact / n,
        "mean_decisions": float(np.mean(decisions)),
        "mean_decisions_to_success": float(np.mean([d for s, d in zip(success, decisions) if s]))
        if any(success)
        else None,
        "stage_reached": {str(k): reach.get(k, 0) for k in range(stages + 1)},
        "outcomes": dict(Counter(str(e["reason"]) for e in episodes)),
        "refusals": int(sum(int(e.get("refusals", 0)) for e in episodes)),
        "undecided": int(sum(int(e.get("undecided", 0)) for e in episodes)),
        **_first_choice(episodes),
    }


def _first_choice(episodes: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Accuracy of the first decision, overall and per hidden route: the only decision of the
    route cue that needs the vanished cue. Empty when episodes carry no first choice."""
    rows = [e for e in episodes if e.get("first_choice") and e["first_choice"].get("required") is not None]
    if not rows:
        return {}
    right = [int(e["first_choice"]["action"] == e["first_choice"]["required"]) for e in rows]
    by_route: dict[str, list[int]] = {}
    for e, r in zip(rows, right):
        by_route.setdefault(str(e.get("route")), []).append(r)
    return {
        "first_choice_accuracy": sum(right) / len(right),
        "first_choice_by_route": {k: sum(v) / len(v) for k, v in sorted(by_route.items())},
    }


def paired_bootstrap(
    candidate: Sequence[float],
    control: Sequence[float],
    *,
    resamples: int = 10_000,
    seed: int = 31012,
) -> dict[str, Any]:
    """Founder-paired mean difference with a percentile bootstrap over founders and a sign count."""
    a = np.asarray(candidate, dtype=float)
    b = np.asarray(control, dtype=float)
    if a.shape != b.shape or a.ndim != 1 or len(a) == 0:
        raise ValueError("paired founder vectors of equal nonzero length are required")
    diff = a - b
    rng = np.random.default_rng(seed)
    index = rng.integers(len(diff), size=(resamples, len(diff)))
    means = diff[index].mean(axis=1)
    low, high = np.quantile(means, [0.025, 0.975])
    return {
        "founders": int(len(diff)),
        "mean_difference": float(diff.mean()),
        "bootstrap_95": [float(low), float(high)],
        "positive": int((diff > 0).sum()),
        "negative": int((diff < 0).sum()),
        "zero": int((diff == 0).sum()),
        "analysis_seed": seed,
        "resamples": resamples,
    }


def policy_from_activation(motor: np.ndarray, temperature: float) -> dict[str, Any]:
    """Greedy choice, margin and the softmax sampling distribution of one settled readout."""
    a = np.asarray(motor, dtype=float).reshape(-1)
    order = np.argsort(-a, kind="stable")
    z = (a - a.max()) / temperature
    p = np.exp(z) / np.exp(z).sum()
    return {
        "greedy": int(order[0]),
        "margin": float(a[order[0]] - a[order[1]]) if len(a) > 1 else float("inf"),
        "probabilities": [float(v) for v in p],
        "activation": [float(v) for v in a],
    }


def sampled_ceiling(actions: int, temperature: float, low: float, high: float, choices: int) -> float:
    """The largest probability a softmax readout with activations in ``[low, high]`` can give
    a sequence of ``choices`` sampled correct actions: no sampled gate may exceed it."""
    single = 1.0 / (1.0 + (actions - 1) * math.exp(-(high - low) / temperature))
    return single**choices
