from darwinmcp.lineage.graph import LineageGraph
from darwinmcp.lineage.svg import render_svg


def test_lineage_add_root_and_child():
    g = LineageGraph()
    r = g.add_root("seed", fitness=0.5)
    c = g.add_child(r, "child", fitness=0.7)
    assert r != c
    assert len(g) == 2
    assert g.graph.has_edge(r, c)


def test_lineage_deterministic_ids():
    g1 = LineageGraph()
    g2 = LineageGraph()
    assert g1.add_root("seed") == g2.add_root("seed")


def test_svg_renders_nonempty():
    g = LineageGraph()
    r = g.add_root("seed", 0.1)
    g.add_child(r, "child", 0.5)
    svg = render_svg(g)
    assert svg.startswith("<svg")
    assert "fitness=" in svg


def test_svg_empty_graph():
    svg = render_svg(LineageGraph())
    assert "empty" in svg.lower()
