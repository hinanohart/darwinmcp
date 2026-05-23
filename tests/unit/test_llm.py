import pytest

from darwinmcp.evolve.llm import DummyLLM, HFInferenceLLM, get_backend


def test_dummy_is_deterministic_per_counter():
    a, b = DummyLLM(), DummyLLM()
    # Each backend instance has its own counter, but for the same call sequence
    # the outputs match.
    assert a.propose_diff("x", "y") == b.propose_diff("x", "y")


def test_dummy_advances_counter():
    llm = DummyLLM()
    d1 = llm.propose_diff("seed", "h")
    d2 = llm.propose_diff("seed", "h")
    assert d1 != d2, "counter must advance between calls"


def test_get_backend_dummy_works():
    assert isinstance(get_backend("dummy"), DummyLLM)


def test_get_backend_hf_refuses_in_v0_1():
    # INV: HF backend must fail loudly in v0.1, never silently no-op.
    with pytest.raises((RuntimeError, NotImplementedError)):
        HFInferenceLLM()


def test_get_backend_unknown_raises():
    with pytest.raises(ValueError):
        get_backend("nope")
