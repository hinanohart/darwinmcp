"""Seed MCP server — STRUCTURAL PLACEHOLDER (the only one in the v0.1 wheel).

This file is the *target* of mutation in the v0.1 evolve loop. Concretely:

    seed/fs_tool/server.py  --(generation N mutation)-->  variant code string
                                                            |
                                            scored by HelloWorldTask (= syntactic)
                                                            |
                                          lineage edge + tool-call trace recorded

The placeholder body below is intentionally minimal: a stub MCP server with one
`fs_read` tool that always returns NotImplementedError. **This is the ONLY place
in the project where NotImplementedError is permitted** (CI invariant INV-1).

Why a placeholder and not a real fs_read? Three reasons:
  1. Real fs_read implementations require host-specific path validation that
     belongs outside the evolve loop (the user picks their own); shipping one
     would create false expectations.
  2. The seed's job is to be *the mutation target*. A trivial baseline makes
     `evolve` runs visibly converge from "raises" → "returns".
  3. INV-1 enforces that EVERY other module has a working implementation. So
     this placeholder is the *signal*, not noise: anywhere else you see
     NotImplementedError outside `evolve/llm.py:HFInferenceLLM` (a v0.2-deferred
     backend with a CLI-time guard), CI is broken.

See README "Honest Marketing" for the full marketing-vs-code contract.
"""

from __future__ import annotations


def fs_read(path: str) -> str:
    """Placeholder fs_read tool — replaced by evolved variants in the loop."""
    raise NotImplementedError("seed placeholder — evolve will replace this body")


def serve() -> None:
    """Entry point for running this seed as a standalone MCP server.

    Wired in v0.2 when the docker sandbox lands; in v0.1 the seed is only
    ever instantiated as a *code string* inside the evolve loop, never run
    as an actual stdio MCP server.
    """
    raise NotImplementedError("seed placeholder — standalone serve() is a v0.2 feature")


if __name__ == "__main__":  # pragma: no cover
    serve()
