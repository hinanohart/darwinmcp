"""Fuzz the INV-2 honest-marketing regex against the bypass paths the
v0.1.0a3 meta-audit (Agent C) flagged.

If a future contributor relaxes `bootstrap/honest_marketing.py` and the
regex loses coverage on a pattern listed here, this file fails first.
"""

from __future__ import annotations

import pytest

from darwinmcp.bootstrap.honest_marketing import check_readme_numbers

# Patterns that MUST be flagged (claim-shaped, no allow-context token nearby).
_BAD_PATTERNS = [
    ("Resolves 76.8% of tasks", "number-then-%"),
    ("99.9 pct accuracy", "decimal then pct"),
    ("Score: 76.8", "unit-before-number colon"),
    ("accuracy 76.8", "unit-before-number space"),
    ("Achieves 50.5% on the bench", "achieves verb"),
    ("Wins 12.3%", "wins verb"),
    ("Resolve rate 88.4%", "multi-word unit"),
    ("Score=76.8", "unit equals number"),
]


# Patterns that MUST NOT be flagged (version strings, license IDs, badge URLs,
# or allow-context-token-accompanied claims).
_OK_PATTERNS = [
    ("Python 3.11+", "version string"),
    ("Apache 2.0", "license identifier"),
    ("v0.1.0a3", "package version"),
    ("![badge-3.11%2B-blue]", "URL hex escape lookahead"),
    ("Score: 76.8 (未測定)", "unmeasured annotation"),
    ("76.8% TBD pending Phase 1", "TBD annotation"),
    ("76.8% (illustrative)", "illustrative annotation"),
    ("3.11", "bare version decimal"),
]


@pytest.mark.parametrize("text,reason", _BAD_PATTERNS)
def test_claim_shape_is_flagged(text: str, reason: str) -> None:
    violations = check_readme_numbers(text, ledger={})
    assert violations, f"INV-2 regex missed {reason!r}: {text!r}"


@pytest.mark.parametrize("text,reason", _OK_PATTERNS)
def test_safe_pattern_does_not_false_positive(text: str, reason: str) -> None:
    violations = check_readme_numbers(text, ledger={})
    assert not violations, f"INV-2 regex false-positive on {reason!r}: {text!r}"
