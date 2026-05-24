"""Honest-marketing README enforcement (INV-2).

The grep is intentionally narrower than "every decimal in the README": it
matches numbers that look like *benchmark claims* (percentages, scored
points, accuracy-style suffixes) while leaving version numbers, license
identifiers ("Apache 2.0"), and Python-version strings ("3.11") alone.

This is the spec from `project_evomcp_unified_synthesis_2026-05-24` INV-2,
adapted so we do not need a whitelist (whitelists are explicitly forbidden
by `feedback_ship-and-yank-lesson-2026-05-23`).
"""

from __future__ import annotations

import re

# Two claim-shape patterns, both anchored by a unit token:
#   _CLAIM_RE_NUM_UNIT — "76.8% accuracy", "99.9 percent", "76.8 score"
#   _CLAIM_RE_UNIT_NUM — "Score: 76.8", "accuracy 76.8", "resolves 76.8%"
# Pure version-style decimals ("0.1.0a1", "3.11", "Apache 2.0") are NOT matched
# because the unit token is absent. The `%(?![\dA-Fa-f])` negative lookahead
# excludes URL-percent-escapes like `%2B` (badge URLs).
_UNIT_TOKEN = (
    r"(?:%(?![\dA-Fa-f])|％|"
    r"\bpercent\b|\bpoints?\b|\bpts\b|\bpct\b|\bscore\b|"
    r"\baccuracy\b|\bresolve\s+rate\b|\bresolves?\b|\bachieves?\b|\bwins?\b)"
)
# Pre-/post-fix shapes:
_CLAIM_RE_NUM_UNIT = re.compile(
    r"(?<!\d)(?P<num>\d{1,4}(?:\.\d+)?)\s*(?P<unit>" + _UNIT_TOKEN + r")",
    re.IGNORECASE,
)
_CLAIM_RE_UNIT_NUM = re.compile(
    r"(?P<unit>\b(?:score|accuracy|resolves?|achieves?|wins?|resolve\s+rate)\b)\s*[:=]?\s*"
    r"(?P<num>\d{1,4}(?:\.\d+)?)\s*%?",
    re.IGNORECASE,
)

_ALLOW_CONTEXT_TOKENS = (
    "未測定",
    "TBD",
    "example",
    "illustrative",
    "reference only",
    "no benchmark numbers",
    "currently passes while the ledger is empty",
    "honest marketing",
)


def check_readme_numbers(readme: str, ledger: dict) -> list[dict]:
    """Return a list of violations (empty list = OK)."""
    violations: list[dict] = []
    seen: set[tuple[int, str]] = set()
    for regex in (_CLAIM_RE_NUM_UNIT, _CLAIM_RE_UNIT_NUM):
        for m in regex.finditer(readme):
            num = m.group("num")
            key = (m.start("num"), num)
            if key in seen:
                continue
            seen.add(key)
            ctx_start = max(0, m.start() - 80)
            ctx_end = min(len(readme), m.end() + 80)
            ctx = readme[ctx_start:ctx_end]
            if num in ledger:
                continue
            if any(tok.lower() in ctx.lower() for tok in _ALLOW_CONTEXT_TOKENS):
                continue
            violations.append({"value": num, "unit": m.group("unit"), "context": ctx})
    return violations
