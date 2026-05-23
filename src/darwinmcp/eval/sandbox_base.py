"""Sandbox ABC — plugin point P3.

Concrete sandboxes isolate the execution of a FitnessTask's probe so a
malicious or merely broken variant cannot affect the host process or
evolution state.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .fitness_base import FitnessTask


class Sandbox(ABC):
    """Abstract isolated runner. Plugin point P3.

    Implementations bundled with darwinmcp:
      - `SubprocessSandbox` (Phase 0; bundled): runs the probe in a fresh
        `python -I -c '<probe>'` subprocess with a wall-clock timeout.
      - `OpenHandsSandbox` (Phase 1; **opt-in, not bundled**): wraps the
        `openhands-tools` runtime — pending LICENSE confirmation, see
        `R18_LICENSE_CHECK.md`.
      - `DockerSandbox` (Phase 2): full container isolation.
    """

    name: str = "abstract"

    @abstractmethod
    def run(self, task: FitnessTask, variant_code: str, logger) -> float:
        """Execute `task.probe(variant_code)` in isolation; return the score."""
