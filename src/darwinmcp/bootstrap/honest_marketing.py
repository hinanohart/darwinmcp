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

# A "claim-shaped" number: N.N (or NN.N) optionally followed by a unit token
# that strongly implies a benchmark figure. Pure version-style decimals like
# "0.1.0a1", "3.11", or "Apache 2.0" are NOT matched. The `%(?![\dA-Fa-f])`
# negative lookahead excludes URL-percent-escapes like `%2B` (badge URLs).
_CLAIM_RE = re.compile(
    r"(?<!\d)(?P<num>\d{1,3}\.\d+)\s*(?P<unit>%(?![\dA-Fa-f])|\bpercent\b|\bpoints?\b|\bpct\b|\bscore\b|\baccuracy\b|\bresolve\s+rate\b)",
    re.IGNORECASE,
)

_ALLOW_CONTEXT_TOKENS = ("未測定", "TBD", "example", "illustrative", "reference only")


def check_readme_numbers(readme: str, ledger: dict) -> list[dict]:
    """Return a list of violations (empty list = OK)."""
    violations: list[dict] = []
    for m in _CLAIM_RE.finditer(readme):
        num = m.group("num")
        ctx_start = max(0, m.start() - 60)
        ctx_end = min(len(readme), m.end() + 60)
        ctx = readme[ctx_start:ctx_end]
        if num in ledger:
            continue
        if any(tok.lower() in ctx.lower() for tok in _ALLOW_CONTEXT_TOKENS):
            continue
        violations.append({"value": num, "unit": m.group("unit"), "context": ctx})
    return violations
