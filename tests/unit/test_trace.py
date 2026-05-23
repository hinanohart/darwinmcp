from darwinmcp.trace.tool_call_logger import ToolCallLogger


def test_logger_records_and_dumps():
    log = ToolCallLogger()
    log.log_call("t", "pass", elapsed_s=0.01, stdout="PASS")
    log.log_call("t", "fail", elapsed_s=0.02, stderr="oops")
    d = log.dump()
    assert len(d) == 2
    assert d[0]["outcome"] == "pass"
    assert d[1]["outcome"] == "fail"
    assert "wall_time" in d[0]
