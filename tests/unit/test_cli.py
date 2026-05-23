import json
import os
from pathlib import Path

from darwinmcp.cli import main


def _run_in(tmp: Path, *argv: str) -> int:
    cwd = os.getcwd()
    os.chdir(tmp)
    try:
        return main(list(argv))
    finally:
        os.chdir(cwd)


def test_cli_version(capsys):
    rc = main(["version"])
    assert rc == 0
    out = capsys.readouterr().out.strip()
    assert out  # non-empty


def test_cli_init_writes_progress(tmp_path: Path):
    rc = _run_in(tmp_path, "init")
    assert rc == 0
    path = tmp_path / ".darwinmcp-progress.json"
    assert path.exists()
    raw = json.loads(path.read_text())
    assert raw["project"] == "darwinmcp"
    assert raw["current_step"] == "P0"


def test_cli_init_refuses_overwrite_without_force(tmp_path: Path):
    _run_in(tmp_path, "init")
    rc = _run_in(tmp_path, "init")
    assert rc != 0


def test_cli_init_force(tmp_path: Path):
    _run_in(tmp_path, "init")
    rc = _run_in(tmp_path, "init", "--force")
    assert rc == 0


def test_cli_verify_passes_on_pre_alpha_readme(tmp_path: Path):
    (tmp_path / "README.md").write_text("# project\nApache 2.0 license. Python 3.11. Pre-alpha.\n")
    rc = _run_in(tmp_path, "verify")
    assert rc == 0
