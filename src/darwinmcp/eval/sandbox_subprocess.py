"""Subprocess-based sandbox — Phase 0 default, zero external deps.

Trade-offs (documented honestly per `feedback_ship-and-yank-lesson`):
  + No docker, no openhands-tools (license-pending), works on any host with
    a Python 3.11+ interpreter.
  + Wall-clock timeout caps runaway variants.
  + Fresh process per probe ⇒ no in-process state leakage.
  - **NOT a security boundary.** A malicious variant can still read $HOME,
    spawn processes, hit the network. v0.1 is targeted at the developer's
    own machine, not at untrusted code. v0.2 ships a docker-based sandbox.
"""

from __future__ import annotations

import subprocess
import sys
import time

from .fitness_base import FitnessTask
from .sandbox_base import Sandbox


class SubprocessSandbox(Sandbox):
    """Runs probes in a fresh `python -I -c ...` subprocess."""

    name = "subprocess"

    def __init__(self, timeout_s: float = 5.0, memory_mb: int = 256) -> None:
        self.timeout_s = timeout_s
        self.memory_mb = memory_mb

    def _preexec(self) -> None:  # pragma: no cover — Linux-only, runs in child
        # Best-effort address-space cap on Linux. Not a security boundary
        # (see module docstring), but a fork bomb / runaway allocator from
        # a malformed variant now hits ~256 MiB instead of host memory.
        if not sys.platform.startswith("linux"):
            return
        try:
            import resource  # noqa: PLC0415 — Linux-only

            cap = self.memory_mb << 20
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
        except (ImportError, ValueError, OSError):
            pass

    def run(self, task: FitnessTask, variant_code: str, logger) -> float:
        probe = task.probe(variant_code)
        started = time.monotonic()
        preexec = self._preexec if sys.platform.startswith("linux") else None
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "-c", probe],
                capture_output=True,
                text=True,
                timeout=self.timeout_s,
                check=False,
                preexec_fn=preexec,
            )
        except subprocess.TimeoutExpired:
            logger.log_call(
                task_name=task.name,
                outcome="timeout",
                elapsed_s=self.timeout_s,
                stdout="",
                stderr="<timeout>",
            )
            return 0.0

        elapsed = time.monotonic() - started
        stdout = (proc.stdout or "").strip()
        ok = stdout.endswith("PASS") and proc.returncode == 0
        outcome = "pass" if ok else "fail"
        logger.log_call(
            task_name=task.name,
            outcome=outcome,
            elapsed_s=elapsed,
            stdout=stdout,
            stderr=(proc.stderr or "").strip(),
        )
        return 1.0 if ok else 0.0
