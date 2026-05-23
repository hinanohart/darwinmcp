from darwinmcp.bootstrap.honest_marketing import check_readme_numbers


def test_version_strings_are_not_flagged():
    readme = "Requires Python 3.11. License: Apache 2.0. darwinmcp 0.1.0a1."
    assert check_readme_numbers(readme, ledger={}) == []


def test_unmeasured_pct_is_flagged():
    readme = "Resolves 76.8% of SWE-bench tasks."
    violations = check_readme_numbers(readme, ledger={})
    assert len(violations) == 1
    assert violations[0]["value"] == "76.8"


def test_ledger_allowlists_a_number():
    readme = "Resolves 76.8% of SWE-bench tasks."
    assert check_readme_numbers(readme, ledger={"76.8": "v0.1.0-actual-run-2026-05-24"}) == []


def test_context_token_allowlists_a_number():
    readme = "Future target: 76.8% (illustrative)."
    assert check_readme_numbers(readme, ledger={}) == []


def test_tbd_context_allowlists_a_number():
    readme = "Score: 99.9% — TBD."
    assert check_readme_numbers(readme, ledger={}) == []
