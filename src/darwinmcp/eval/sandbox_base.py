"""Sandbox ABC — plugin point P3.

Concrete sandboxes run a FitnessTask's probe in a separate process so a
broken variant cannot corrupt the host process or evolution state. The
strength of the isolation is implementation-defined: the bundled Phase 0
`SubprocessSandbox` is process-level (env scrub + temp cwd + resource caps)
but does NOT isolate the network or the wider filesystem. Strong isolation
arrives with the Phase 2 `DockerSandbox`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .fitness_base import FitnessTask


class Sandbox(ABC):
    """Abstract isolated runner. Plugin point P3.

    Guarantees are per implementation; see each subclass docstring for what is
    and is not isolated. Implementations bundled with darwinmcp:
      - `SubprocessSandbox` (Phase 0; bundled): runs the probe in a fresh
        `python -I -c '<probe>'` subprocess with a wall-clock timeout, a
        scrubbed env (no host credentials), an isolated temp cwd, and
        best-effort resource caps. Network is NOT isolated.
      - `OpenHandsSandbox` (Phase 1; **opt-in, not bundled**): wraps the
        `openhands-tools` runtime — pending LICENSE confirmation, see
        `R18_LICENSE_CHECK.md`.
      - `DockerSandbox` (Phase 2): full container isolation.
    """

    name: str = "abstract"

    @abstractmethod
    def run(self, task: FitnessTask, variant_code: str, logger) -> float:
        """Execute `task.probe(variant_code)` in isolation; return the score."""
