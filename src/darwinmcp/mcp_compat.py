"""MCP-spec compatibility shim.

Why this exists: the MCP spec is on a v1 → v2 trajectory (`mcp` PyPI README
says "the current plan is to work through v2 and have it released some time
in Q1"). The 2026-07-28 RC introduces "Tasks/Apps" which may absorb some of
darwinmcp's evolve-server concerns. We isolate the spec touch-points here
so a v2 bump (or a fork-pin if v2 silently obsoletes us) is a one-file
change, not a project-wide refactor.
"""

from __future__ import annotations

import importlib.metadata
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MCPVersion:
    major: int
    minor: int
    patch: int

    @property
    def is_v1(self) -> bool:
        return self.major == 1

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def detected_mcp_version() -> MCPVersion:
    """Return the installed `mcp` package version, or 0.0.0 if not installed."""
    try:
        raw = importlib.metadata.version("mcp")
    except importlib.metadata.PackageNotFoundError:
        return MCPVersion(0, 0, 0)
    parts = raw.split(".")[:3]
    while len(parts) < 3:
        parts.append("0")
    try:
        return MCPVersion(
            int(parts[0]),
            int(parts[1]),
            int(parts[2].split("a")[0].split("b")[0].split("rc")[0] or 0),
        )
    except ValueError:
        return MCPVersion(0, 0, 0)


def assert_compatible() -> None:
    """Raise if the installed MCP version is outside the v0.1 supported range."""
    v = detected_mcp_version()
    if not v.is_v1:
        raise RuntimeError(
            f"darwinmcp v0.1 supports mcp v1.x only; detected {v}. "
            "Pin `mcp>=1.25,<2` until darwinmcp v0.2 (which targets v2)."
        )
