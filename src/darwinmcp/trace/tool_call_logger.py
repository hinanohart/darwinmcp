"""ToolCallLogger — append-only structured log of per-variant tool calls.

The sandbox calls `log_call(...)` for every probe execution; the result is
serialised to disk at the end of an `evolve` run and consumed by the
CircuitMap α renderer.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field


@dataclass(frozen=True, slots=True)
class ToolCallEvent:
    task_name: str
    outcome: str  # "pass" | "fail" | "timeout"
    elapsed_s: float
    stdout: str
    stderr: str
    wall_time: float  # unix epoch seconds


@dataclass(slots=True)
class ToolCallLogger:
    events: list[ToolCallEvent] = field(default_factory=list)

    def log_call(
        self,
        task_name: str,
        outcome: str,
        elapsed_s: float,
        stdout: str = "",
        stderr: str = "",
    ) -> None:
        self.events.append(
            ToolCallEvent(
                task_name=task_name,
                outcome=outcome,
                elapsed_s=elapsed_s,
                stdout=stdout,
                stderr=stderr,
                wall_time=time.time(),
            )
        )

    def dump(self) -> list[dict]:
        return [asdict(e) for e in self.events]
