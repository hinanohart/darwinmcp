"""CircuitMap α — 2-axis interpretability (lineage × tool-call trace).

Phase 2 fills in the actual attribution computation. v0.1 ships the data
class and a stub `compute` so callers can build against the v0.1 API
without v0.2 churn. `compute` returns a structurally-valid but empty
table (`cells == {}`); no attribution numbers are produced. Downstream
renderers should treat `cells == {}` as "(α v0.2 stub — no attribution
yet)" rather than as a meaningful zero.

NOTE: per the synthesis decision (`project_evomcp_unified_synthesis_…`),
v0.1 has ONLY 2 axes; the 3rd axis (cross-layer transcoder attribution)
is explicitly v0.2 backlog. Do not invent a 3rd axis here.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .graph import LineageGraph


@dataclass(slots=True)
class CircuitMapAlpha:
    """2-axis attribution table: lineage node × tool-call event."""

    lineage_node_ids: list[str] = field(default_factory=list)
    tool_call_ids: list[str] = field(default_factory=list)
    # `cells[(lineage_id, tool_id)] = attribution_score`. Empty in v0.1.
    cells: dict[tuple[str, str], float] = field(default_factory=dict)
    # `measured == True` only when `cells` contains REAL ablation attribution
    # numbers. v0.1 always leaves this False so any Phase-2 PR that fills
    # `cells` without flipping the flag fails the INV-6 check by construction.
    measured: bool = False

    @classmethod
    def compute(cls, lineage: LineageGraph, trace_events: list[dict]) -> CircuitMapAlpha:
        """Compute the 2-axis attribution table.

        v0.1: stub. v0.2 (Phase 2) wires this to a real attribution pass.
        Until then the function returns a structurally-valid but empty table
        (`cells == {}`, `measured is False`), which the SVG renderer prints as
        "(α v0.2 stub — no attribution yet)".
        """
        return cls(
            lineage_node_ids=list(lineage.graph.nodes),
            tool_call_ids=[str(i) for i in range(len(trace_events))],
            cells={},
            measured=False,
        )
