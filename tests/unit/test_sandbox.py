import os

from darwinmcp.eval.fitness_base import FitnessTask
from darwinmcp.eval.fitness_tasks import HelloWorldTask
from darwinmcp.eval.sandbox_subprocess import SubprocessSandbox
from darwinmcp.trace.tool_call_logger import ToolCallLogger


class _EnvProbeTask(FitnessTask):
    """Probe that PASSes only if the named env var is *absent* in the child."""

    name = "env_probe"

    def __init__(self, var: str) -> None:
        self._var = var

    def probe(self, variant_code: str) -> str:
        return f"import os\nprint('PASS' if {self._var!r} not in os.environ else 'FAIL: leaked')\n"


def test_subprocess_sandbox_scrubs_credential_env(monkeypatch):
    # Plant a credential-shaped var in the host env; it must NOT reach the child.
    monkeypatch.setenv("HF_TOKEN", "planted-secret-should-not-leak")
    assert os.environ["HF_TOKEN"] == "planted-secret-should-not-leak"

    sb = SubprocessSandbox(timeout_s=10.0)
    logger = ToolCallLogger()
    score = sb.run(_EnvProbeTask("HF_TOKEN"), "", logger)

    assert score == 1.0, f"credential var leaked to child: {logger.events[0].stdout!r}"
    assert logger.events[0].outcome == "pass"


def test_subprocess_sandbox_passes_valid_code():
    sb = SubprocessSandbox(timeout_s=10.0)
    logger = ToolCallLogger()
    score = sb.run(HelloWorldTask(), "x = 1\n", logger)
    assert score == 1.0
    assert len(logger.events) == 1
    assert logger.events[0].outcome == "pass"


def test_subprocess_sandbox_fails_invalid_code():
    sb = SubprocessSandbox(timeout_s=10.0)
    logger = ToolCallLogger()
    score = sb.run(HelloWorldTask(), "def f(:\n", logger)  # syntax error
    assert score == 0.0
    assert logger.events[0].outcome == "fail"
