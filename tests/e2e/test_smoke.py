"""E2E smoke — runs the full evolve loop with DummyLLM × 1 generation.

This is the test that the README claims runs on `pip install`. If it breaks,
the release is yanked. Tagged `e2e` so it can be selected/excluded explicitly.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from darwinmcp.cli import main


@pytest.mark.e2e
def test_smoke_end_to_end(tmp_path: Path):
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        rc_init = main(["init"])
        assert rc_init == 0

        rc_evolve = main(["evolve", "--generations", "1", "--backend", "dummy"])
        assert rc_evolve == 0
    finally:
        os.chdir(cwd)

    progress_path = tmp_path / ".darwinmcp-progress.json"
    assert progress_path.exists()
    raw = json.loads(progress_path.read_text())
    assert raw["generation"] == 1
    assert raw["fitness_tasks_count"] >= 1
    assert raw["last_smoke_test_passed"] is True

    trace_path = tmp_path / "runs" / "trace.json"
    assert trace_path.exists()
    trace = json.loads(trace_path.read_text())
    assert len(trace) >= 1
    assert trace[0]["outcome"] in {"pass", "fail", "timeout"}
