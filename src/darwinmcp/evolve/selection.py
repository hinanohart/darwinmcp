"""Selection: pick top-N variants by fitness for the next generation.

Phase-0: trivial top-1. Phase-1: tournament / Pareto front candidates land here.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScoredVariant:
    variant_id: str
    code: str
    fitness: float


def top_n(scored: Iterable[ScoredVariant], n: int = 1) -> list[ScoredVariant]:
    """Return the top-`n` variants by fitness (descending)."""
    return sorted(scored, key=lambda v: v.fitness, reverse=True)[:n]
