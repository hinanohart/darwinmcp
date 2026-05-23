"""LLM backend ABC + Phase-0 implementations.

- `LLMBackend` — ABC every backend must satisfy.
- `DummyLLM` — deterministic, network-free, returns a hint-derived snippet.
  This is the **default** in v0.1 and is what the smoke test exercises.
- `HFInferenceLLM` — stub for v0.2; raises a clearly-marked NotImplementedError.
  This is the ONLY allowed NotImplementedError outside `seed/fs_tool/` (INV-1
  exception) because it represents a v0.2-deferred backend, not a placeholder
  in the run path — `get_backend("hf")` errors loudly at CLI parse time, not
  at evolve time, so the user cannot mistake it for working.
"""

from __future__ import annotations

import hashlib
import os
from abc import ABC, abstractmethod


class LLMBackend(ABC):
    """Abstract LLM backend used by the evolve loop.

    Concrete backends produce a short "diff hint" string given the current
    seed code and a high-level mutation hint. The mutator splices the hint
    into the seed; backends do not edit code directly.
    """

    name: str = "abstract"

    @abstractmethod
    def propose_diff(self, seed_code: str, hint: str) -> str:
        """Return a short snippet describing a proposed mutation."""


class DummyLLM(LLMBackend):
    """Deterministic, network-free backend. Always usable, no token required.

    The "diff" is a short hash digest of (seed_code, hint, generation_counter).
    This is sufficient to make `evolve` advance and write a non-trivial trace,
    while making it impossible to misread Phase-0 fitness scores as "real LLM
    performance."
    """

    name = "dummy"

    def __init__(self) -> None:
        self._counter = 0

    def propose_diff(self, seed_code: str, hint: str) -> str:
        self._counter += 1
        payload = f"{seed_code}\n{hint}\n{self._counter}".encode()
        digest = hashlib.sha256(payload).hexdigest()[:12]
        return f"hint={hint!r} digest={digest}"


class HFInferenceLLM(LLMBackend):
    """HuggingFace Inference API backend — STUB in v0.1.

    Wired in v0.2. We deliberately fail at construction (not at call time)
    so misuse is caught by the CLI before any evolve loop starts.
    """

    name = "hf"

    def __init__(self, model: str = "Qwen/Qwen2.5-Coder-32B-Instruct") -> None:
        # Unified failure path: regardless of HF_TOKEN, v0.1 does NOT implement
        # HF inference. A single NotImplementedError prevents the saelet-style
        # UX trap where "set the env var and it works" leads to silent fallback.
        # INV-1: this is the ONE allowed non-seed NotImplementedError; the
        # `tests/honest_marketing/test_inv1_no_extra_placeholders.py` exempts
        # this file explicitly, and the CI grep guard mirrors that allowlist.
        del model  # held for v0.2 API compatibility
        _ = os.environ.get("HF_TOKEN")  # documented input, not used in v0.1
        raise NotImplementedError(
            "HFInferenceLLM is deferred to v0.2. v0.1 ships --backend dummy only."
        )

    def propose_diff(self, seed_code: str, hint: str) -> str:  # pragma: no cover
        raise NotImplementedError("v0.2")


def get_backend(name: str) -> LLMBackend:
    """CLI helper: map a backend name string to a backend instance."""
    if name == "dummy":
        return DummyLLM()
    if name == "hf":
        return HFInferenceLLM()
    raise ValueError(f"unknown backend: {name!r}")
