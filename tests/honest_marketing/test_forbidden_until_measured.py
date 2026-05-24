"""Make `ProgressV2.forbidden_until_measured` actually do something.

v0.1.0a3 meta-audit (Agent A finding M-5): the list of forbidden metric
tokens was data-only — no source path ever grepped for them. This test
fails if any of those tokens appear in README.md or CHANGELOG.md without an
allow-context word in the surrounding 80 chars.

The tokens are deliberately bare names (`swe_bench_resolve_rate` etc.) so
that prose like "we will report swe_bench_resolve_rate in v0.2" passes
(because the token is qualified as a future plan) while a sneaky
`swe_bench_resolve_rate: 0.768` would fail.
"""

from __future__ import annotations

import re
from pathlib import Path

from darwinmcp.bootstrap.progress import ProgressV2

REPO_ROOT = Path(__file__).resolve().parents[2]

_ALLOW = (
    "未測定",
    "TBD",
    "v0.2",
    "Phase 1",
    "Phase 2",
    "forbidden_until_measured",
    "honest marketing",
    "no benchmark numbers",
    "backlog",
    "deferred",
)


def _scan(text: str, tokens: list[str]) -> list[tuple[str, str]]:
    violations: list[tuple[str, str]] = []
    for tok in tokens:
        for m in re.finditer(re.escape(tok), text):
            # ±200 chars: enough to catch the "honest marketing" / "v0.2 backlog"
            # framing words that legitimately introduce a forbidden token in a
            # CHANGELOG / README paragraph; smaller windows produced false
            # positives where the framing word was 90-150 chars away.
            ctx = text[max(0, m.start() - 200) : min(len(text), m.end() + 200)]
            if any(a.lower() in ctx.lower() for a in _ALLOW):
                continue
            violations.append((tok, ctx))
    return violations


def test_forbidden_tokens_never_appear_unguarded_in_readme() -> None:
    readme = (REPO_ROOT / "README.md").read_text()
    violations = _scan(readme, ProgressV2().forbidden_until_measured)
    assert not violations, (
        f"forbidden_until_measured leak in README without allow-context: {violations}"
    )


def test_forbidden_tokens_never_appear_unguarded_in_changelog() -> None:
    cl = (REPO_ROOT / "CHANGELOG.md").read_text()
    violations = _scan(cl, ProgressV2().forbidden_until_measured)
    assert not violations, (
        f"forbidden_until_measured leak in CHANGELOG without allow-context: {violations}"
    )
