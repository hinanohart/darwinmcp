"""INV-1: `NotImplementedError` is forbidden outside the seed placeholder
and the v0.2-deferred HF backend (which is the only allowed non-seed exception,
and is guarded by a CLI-time RuntimeError so users cannot silently misuse it)."""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC = _REPO_ROOT / "src" / "darwinmcp"

_ALLOWED_FILES = {
    _SRC / "seed" / "fs_tool" / "server.py",  # the ONE structural placeholder
    _SRC / "evolve" / "llm.py",  # HFInferenceLLM v0.2 stub, CLI-guarded
}


@pytest.mark.honest_marketing
def test_no_extra_notimplementederror_in_src():
    offenders: list[str] = []
    for py in _SRC.rglob("*.py"):
        if py in _ALLOWED_FILES:
            continue
        text = py.read_text()
        if "NotImplementedError" in text:
            offenders.append(str(py.relative_to(_REPO_ROOT)))
    assert not offenders, (
        "INV-1 violation: NotImplementedError found outside the seed placeholder "
        "and the v0.2-deferred HF backend stub:\n  - " + "\n  - ".join(offenders)
    )
