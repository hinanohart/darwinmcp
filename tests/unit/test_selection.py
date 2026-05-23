from darwinmcp.evolve.selection import ScoredVariant, top_n


def test_top_n_orders_desc():
    scored = [
        ScoredVariant("a", "code_a", 0.1),
        ScoredVariant("b", "code_b", 0.9),
        ScoredVariant("c", "code_c", 0.5),
    ]
    top = top_n(scored, n=2)
    assert [v.variant_id for v in top] == ["b", "c"]


def test_top_n_n_eq_zero():
    assert top_n([ScoredVariant("a", "c", 1.0)], n=0) == []
