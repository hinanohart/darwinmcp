import json
from pathlib import Path

from darwinmcp.bootstrap.progress import ProgressV2, read_progress, write_progress


def test_fresh_progress_has_p0(tmp_path: Path):
    p = ProgressV2.fresh()
    assert p.current_step == "P0"
    assert p.project == "darwinmcp"
    assert p.license == "Apache-2.0"
    assert p.repo == "hinanohart/darwinmcp"
    assert "src/darwinmcp/seed/fs_tool/server.py" in p.structural_placeholders


def test_progress_roundtrip(tmp_path: Path):
    path = tmp_path / ".darwinmcp-progress.json"
    p = ProgressV2.fresh()
    p.generation = 3
    p.fitness_tasks_count = 1
    write_progress(path, p)

    raw = json.loads(path.read_text())
    assert raw["$schema_version"] == "2"
    assert raw["generation"] == 3

    p2 = read_progress(path)
    assert p2.generation == 3
    assert p2.fitness_tasks_count == 1
