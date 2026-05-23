"""INV-5: the entry-point `darwinmcp = "darwinmcp.cli:main"` declared in
pyproject.toml must actually resolve (saelet-style cli:main absence prevention)."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.honest_marketing
def test_entry_point_resolves():
    pyproject = tomllib.loads((_REPO_ROOT / "pyproject.toml").read_text())
    scripts = pyproject.get("project", {}).get("scripts", {})
    assert "darwinmcp" in scripts, "pyproject.toml [project.scripts] missing `darwinmcp`"
    target = scripts["darwinmcp"]
    module_path, _, attr = target.partition(":")
    assert attr, f"entry-point {target!r} missing `:attr`"

    mod = __import__(module_path, fromlist=[attr])
    fn = getattr(mod, attr, None)
    assert callable(fn), f"entry-point {target!r} does not resolve to a callable"
