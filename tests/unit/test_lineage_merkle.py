"""INV-4: lineage edges must be merkle-chained (parent hash referenced by
child node MUST match an existing node's content hash).

v0.1's `LineageGraph.add_child` content-addresses every node via sha256 but
does NOT verify that the supplied `parent_id` is an existing node — a buggy
or malicious mutator could fabricate a parent edge undetected.

This test is xfail-marked so it runs green today (acknowledging the gap) and
turns red the moment Phase 1 adds the parent-existence check, at which point
the marker should be removed.
"""

from __future__ import annotations

import pytest

from darwinmcp.lineage.graph import LineageGraph


@pytest.mark.xfail(
    reason=(
        "INV-4: parent-hash merkle chain — Phase 1 will reject add_child "
        "with a parent_id that does not match an existing node's content hash. "
        "Remove this xfail marker when the check lands."
    ),
    strict=False,
)
def test_add_child_rejects_unknown_parent() -> None:
    g = LineageGraph()
    g.add_root("seed code")
    with pytest.raises(ValueError, match="parent"):
        g.add_child("nonexistent_parent_id_xxxxxxxxxx", "variant code", fitness=1.0)
