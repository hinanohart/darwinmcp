from darwinmcp.lineage.circuitmap import CircuitMapAlpha
from darwinmcp.lineage.graph import LineageGraph


def test_circuitmap_alpha_is_structurally_valid_but_empty_in_v01():
    g = LineageGraph()
    g.add_root("seed", 0.1)
    cm = CircuitMapAlpha.compute(g, trace_events=[{"x": 1}, {"x": 2}])
    assert cm.lineage_node_ids
    assert len(cm.tool_call_ids) == 2
    # v0.1 returns an empty cells dict on purpose; the README and CHANGELOG
    # call this out explicitly.
    assert cm.cells == {}
    # INV-6: the `measured` flag must be False as long as `cells` is empty,
    # so a Phase-2 PR that fills `cells` without flipping the flag fails by
    # construction. Added in v0.1.0a3 meta-audit (Agent A finding M-4).
    assert cm.measured is False
