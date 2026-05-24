"""INV-3: fitness must be monotonically non-decreasing across generations,
OR a bootstrap CI must show statistically significant gain.

v0.1 ships ONE generation and ONE task (`HelloWorldTask`), so this invariant
is not yet machine-checkable. The stub below holds the spec slot so Phase 1
cannot ship without an implementation.
"""

from __future__ import annotations

import pytest


@pytest.mark.skip(
    reason=(
        "Phase 1: requires generations >= 3 (and ideally a small evolve "
        "run with bootstrap CI per R5). Implementing this test is one of "
        "the Phase 1 P1 acceptance criteria; do not delete this stub."
    )
)
def test_fitness_monotonic_or_bootstrap_ci_significant() -> None:
    # Implementation outline for Phase 1:
    #   1. Run `darwinmcp evolve --generations 3 --backend dummy` against a
    #      fitness task that DummyLLM can plausibly improve on.
    #   2. Collect per-generation scores from runs/trace.json.
    #   3. Assert either: (a) sorted(scores) == scores, OR
    #      (b) bootstrap CI on score[-1] - score[0] excludes 0.
    raise AssertionError("INV-3 — implemented in Phase 1, see Phase 1 todo")
