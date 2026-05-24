"""Subprocess-based sandbox — Phase 0 default, zero external deps.

Trade-offs (documented honestly per `feedback_ship-and-yank-lesson`):
  + No docker, no openhands-tools (license-pending), works on any host with
    a Python 3.11+ interpreter.
  + Wall-clock timeout caps runaway variants.
  + Fresh process per probe ⇒ no in-process state leakage.
  + The child inherits a scrubbed, minimal env (allowlist only) so host
    credentials in os.environ (HF_TOKEN, OPENAI_API_KEY, AWS_*, …) are not
    handed to variant code, and runs in an isolated temp cwd.
  - **NOT a full security boundary.** The network is NOT isolated and the
    child can still read most of the filesystem (only cwd is sandboxed).
    v0.1 is targeted at the developer's own machine, not at untrusted code.
    v0.2 ships a docker-based sandbox.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time

from .fitness_base import FitnessTask
from .sandbox_base import Sandbox

# Env vars passed through to the child verbatim. Everything else (including
# every credential-like var) is dropped — an allowlist is safer than a
# denylist because new secrets added to the host env stay invisible by default.
_ENV_ALLOWLIST = frozenset(
    {
        "PATH",
        "PYTHONPATH",
        "PYTHONHASHSEED",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "TZ",
        "TMPDIR",
        "SYSTEMROOT",  # Windows: required for the interpreter to start
    }
)

# Belt-and-suspenders: prefixes/names that must never reach the child even if a
# future edit widens the allowlist. Used only to assert the allowlist is clean.
_CREDENTIAL_PREFIXES = ("HF_", "OPENAI_", "AWS_", "ANTHROPIC_", "AZURE_", "GCP_")
_CREDENTIAL_NAMES = frozenset(
    {"HF_TOKEN", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "HUGGINGFACE_TOKEN"}
)


def _scrubbed_env() -> dict[str, str]:
    """Return a minimal env (allowlist) with all credential-like vars dropped."""
    env: dict[str, str] = {
        k: v
        for k, v in os.environ.items()
        if k in _ENV_ALLOWLIST
        and k not in _CREDENTIAL_NAMES
        and not k.startswith(_CREDENTIAL_PREFIXES)
    }
    return env


class SubprocessSandbox(Sandbox):
    """Runs probes in a fresh `python -I -c ...` subprocess."""

    name = "subprocess"

    def __init__(self, timeout_s: float = 5.0, memory_mb: int = 256) -> None:
        self.timeout_s = timeout_s
        self.memory_mb = memory_mb

    def _preexec(self) -> None:  # pragma: no cover — Linux-only, runs in child
        # Best-effort resource caps on Linux. Not a full security boundary
        # (see module docstring), but a fork bomb / runaway allocator / disk
        # filler from a malformed variant now hits a cap instead of the host.
        if not sys.platform.startswith("linux"):
            return
        try:
            import resource  # noqa: PLC0415 — Linux-only

            cap = self.memory_mb << 20
            resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
            # Cap written-file size (~64 MiB) and child process count to blunt
            # disk fillers and fork bombs from a malformed variant.
            fsize = 64 << 20
            resource.setrlimit(resource.RLIMIT_FSIZE, (fsize, fsize))
            resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
        except (ImportError, ValueError, OSError):
            pass

    def run(self, task: FitnessTask, variant_code: str, logger) -> float:
        probe = task.probe(variant_code)
        started = time.monotonic()
        preexec = self._preexec if sys.platform.startswith("linux") else None
        # Isolate the working directory so probes that write relative paths
        # touch a throwaway dir, not the developer's repo/cwd.
        try:
            with tempfile.TemporaryDirectory(prefix="darwinmcp-sandbox-") as cwd:
                proc = subprocess.run(
                    [sys.executable, "-I", "-c", probe],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_s,
                    check=False,
                    preexec_fn=preexec,
                    env=_scrubbed_env(),
                    cwd=cwd,
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
