from darwinmcp.evolve.llm import DummyLLM
from darwinmcp.evolve.mutator import mutate


def test_mutate_extends_seed():
    seed = "x = 1\n"
    out = mutate(seed, DummyLLM(), generation=1)
    assert out.startswith(seed)
    assert "variant gen=1" in out


def test_mutate_distinct_across_generations():
    seed = "x = 1\n"
    llm = DummyLLM()
    a = mutate(seed, llm, generation=1)
    b = mutate(seed, llm, generation=2)
    assert a != b
