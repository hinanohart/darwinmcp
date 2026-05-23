"""LineageGraph — a small DAG over (parent_variant_id → child_variant_id).

Each node carries the variant's code (as a string) and its fitness score.
Identifiers are deterministic sha256(code) prefixes so that re-running the
same evolve loop with the same DummyLLM seed yields the same lineage IDs
(testable, observable, no UUID drift).
"""

from __future__ import annotations

import hashlib

import networkx as nx


def _variant_id(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()[:12]


class LineageGraph:
    """Thin wrapper over `networkx.DiGraph` with darwinmcp-specific helpers."""

    def __init__(self) -> None:
        self._g: nx.DiGraph = nx.DiGraph()

    @property
    def graph(self) -> nx.DiGraph:
        return self._g

    def add_root(self, code: str, fitness: float | None = None) -> str:
        vid = _variant_id(code)
        self._g.add_node(vid, code=code, fitness=fitness, root=True)
        return vid

    def add_child(self, parent_id: str, code: str, fitness: float | None = None) -> str:
        vid = _variant_id(code)
        # If a node with the same code already exists (perfectly deterministic
        # collision) we keep the older one — variant IDs are content-addressed.
        if vid not in self._g:
            self._g.add_node(vid, code=code, fitness=fitness, root=False)
        else:
            # Update fitness only if previously unscored (avoids silent overwrite).
            if self._g.nodes[vid].get("fitness") is None:
                self._g.nodes[vid]["fitness"] = fitness
        self._g.add_edge(parent_id, vid)
        return vid

    def __len__(self) -> int:
        return self._g.number_of_nodes()

    def fitness_trajectory(self) -> list[float]:
        """Return per-node fitness in insertion order, with None replaced by 0.0."""
        return [(self._g.nodes[n].get("fitness") or 0.0) for n in self._g.nodes]
