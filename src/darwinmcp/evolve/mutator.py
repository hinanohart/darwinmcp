"""Mutator: glues an LLMBackend to seed code, producing variant code strings.

Phase-0 implementation: append-only with a `# variant gen=N: …` comment. Phase-1
will diff-apply at line granularity guided by `shinka-evolve`.
"""

from __future__ import annotations

from .llm import LLMBackend


def mutate(seed_code: str, backend: LLMBackend, generation: int, hint: str = "improve") -> str:
    """Return a variant of `seed_code` for the given generation."""
    diff = backend.propose_diff(seed_code, hint)
    return f"{seed_code}\n# variant gen={generation}: {diff}\n"
