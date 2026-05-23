from darwinmcp.eval.fitness_tasks import HelloWorldTask
from darwinmcp.eval.sandbox_subprocess import SubprocessSandbox
from darwinmcp.trace.tool_call_logger import ToolCallLogger


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
