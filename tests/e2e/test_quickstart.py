"""INV-10: `examples/01_hello_evolve.py` must complete in < 30s.

Machine-enforced version of the synthesis spec's "30 秒以内" quickstart budget.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_EXAMPLE = _REPO_ROOT / "examples" / "01_hello_evolve.py"


@pytest.mark.e2e
def test_quickstart_under_30s():
    assert _EXAMPLE.exists(), "examples/01_hello_evolve.py must exist (INV-10)"
    started = time.monotonic()
    proc = subprocess.run(
        [sys.executable, str(_EXAMPLE)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    elapsed = time.monotonic() - started
    assert proc.returncode == 0, f"quickstart failed: stdout={proc.stdout!r} stderr={proc.stderr!r}"
    assert elapsed < 30, f"quickstart took {elapsed:.2f}s, INV-10 budget is 30s"
    assert "OK" in proc.stdout, f"unexpected stdout: {proc.stdout!r}"
