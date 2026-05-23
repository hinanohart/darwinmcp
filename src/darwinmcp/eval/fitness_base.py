"""FitnessTask ABC — plugin point P1.

A concrete FitnessTask describes one self-contained probe used to score a
variant of `server.py`. The contract is intentionally narrow so third-party
tasks can plug in without depending on the internals of the evolve loop.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TaskResult:
    """Outcome of running a single FitnessTask against one variant."""

    score: float  # higher is better; convention: 1.0 = pass, 0.0 = fail
    ok: bool  # True iff the sandbox ran to completion without error
    detail: str  # short human-readable note (one line)


class FitnessTask(ABC):
    """Abstract fitness probe. Plugin point P1.

    A FitnessTask should be:
      - **deterministic** given the same variant_code (essential for INV-3,
        the "fitness monotonically increases or bootstrap-CI is significant"
        invariant);
      - **side-effect free** outside the sandbox provided by the runner;
      - **fast** in Phase 0 (subprocess sandbox budget: ~5 seconds per run).
    """

    name: str = "abstract"

    @abstractmethod
    def probe(self, variant_code: str) -> str:
        """Return the small Python program that the sandbox will execute.

        The program must `print("PASS")` on success and `print("FAIL: <why>")`
        on failure; the sandbox parses stdout to assign the score.
        """
