"""`.darwinmcp-progress.json` schema v2 — compact-restore key for cross-session work.

The structure is the one designed in `project_evomcp_unified_synthesis_2026-05-24`,
renamed to darwinmcp. It is intentionally JSON-serialisable with no nested
dataclasses so it can be read by any tool (`jq`, a future critic agent, etc.).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

SCHEMA_VERSION = "2"


@dataclass(slots=True)
class CircuitBreaker:
    max_attempts_per_step: int = 5
    max_total_hours: int = 240  # 6 weeks ish


@dataclass(slots=True)
class ProgressV2:
    project: str = "darwinmcp"
    current_step: str = "P0"
    completed_steps: list[str] = field(default_factory=list)
    step_started_at: str = ""
    step_attempts: int = 0
    blockers: list[str] = field(default_factory=list)
    circuit_breaker: CircuitBreaker = field(default_factory=CircuitBreaker)
    repo: str = "hinanohart/darwinmcp"
    license: str = "Apache-2.0"
    # Sentinel values document v0.1 dep state for the cross-session progress
    # file. `shinka-evolve` / `openhands-tools` are kept as keys (with explicit
    # "v0.2-deferred-*" markers) so a future critic agent can grep this dict
    # without losing the pivot decision audit trail (see R18_LICENSE_CHECK.md).
    core_deps_locked: dict[str, str] = field(
        default_factory=lambda: {
            "mcp": "TBD-P0",
            "shinka-evolve": "v0.2-deferred-resolver",  # PyPI 0.0.6 vs mcp httpx conflict
            "openhands-tools": "v0.2-deferred-license",  # LICENSE not stated on PyPI
            "huggingface-hub": "TBD-P0",
        }
    )
    hf_default_model: str = "Qwen/Qwen2.5-Coder-32B-Instruct"
    generation: int = 0
    fitness_tasks_count: int = 0
    structural_placeholders: list[str] = field(
        default_factory=lambda: ["src/darwinmcp/seed/fs_tool/server.py"]
    )
    forbidden_until_measured: list[str] = field(
        default_factory=lambda: [
            "swe_bench_resolve_rate",
            "tool_call_success_rate",
            "circuitmap_attribution_score",
        ]
    )
    last_smoke_test_passed: bool = False
    fallback_log: list[str] = field(default_factory=list)
    human_intervention_required: bool = False
    human_intervention_reason: str | None = None
    three_agent_verify_results: dict | None = None
    checkpoints: list[dict] = field(default_factory=list)

    @classmethod
    def fresh(cls, project_name: str = "darwinmcp") -> ProgressV2:
        p = cls(project=project_name)
        p.step_started_at = datetime.now(UTC).isoformat()
        return p

    def to_dict(self) -> dict:
        d = asdict(self)
        d["$schema_version"] = SCHEMA_VERSION
        return d


def write_progress(path: Path, prog: ProgressV2) -> None:
    path.write_text(json.dumps(prog.to_dict(), indent=2, sort_keys=False))


def read_progress(path: Path) -> ProgressV2:
    raw = json.loads(path.read_text())
    raw.pop("$schema_version", None)
    cb_raw = raw.pop("circuit_breaker", None)
    p = ProgressV2(**raw)
    if isinstance(cb_raw, dict):
        p.circuit_breaker = CircuitBreaker(**cb_raw)
    return p
