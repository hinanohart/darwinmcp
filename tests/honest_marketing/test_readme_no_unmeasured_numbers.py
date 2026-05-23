"""INV-2 enforcement on the actual repo README."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from darwinmcp.bootstrap.honest_marketing import check_readme_numbers

_REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.honest_marketing
def test_repo_readme_has_no_unmeasured_claim_numbers():
    readme = (_REPO_ROOT / "README.md").read_text()
    ledger_path = _REPO_ROOT / "docs" / "_ledger.json"
    ledger_raw = json.loads(ledger_path.read_text())
    ledger = ledger_raw.get("measurements", {})
    violations = check_readme_numbers(readme, ledger)
    if violations:
        msg = "\n".join(f"  - {v['value']} ({v['unit']}): …{v['context']!r}…" for v in violations)
        raise AssertionError(
            "README contains claim-shaped numbers without a ledger entry "
            "and without 未測定/TBD/example/illustrative/reference only:\n" + msg
        )
