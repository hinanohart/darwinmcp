# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0a2] — 2026-05-24 (Phase 0 hardening; 3-monitor agent findings)

### Changed
- `cli.py` evolve loop now routes mutations through `evolve.mutator.mutate` (previously inlined). API surface and loop are now identical, removing a dead-code drift the critic monitor flagged.
- `evolve.llm.HFInferenceLLM.__init__` unified to a single `NotImplementedError` regardless of `HF_TOKEN` (previously branched between `RuntimeError` and `NotImplementedError`). This prevents the saelet-style UX trap where "set the env var" looks like it will enable a feature that v0.1 does not ship.
- `pyproject.toml` `description` reworded from "SWE-bench-style sandbox fitness" → "subprocess sandbox fitness (SWE-bench Verified adapter is v0.2 backlog)" to prevent PyPI-page misread.
- `bootstrap/progress.py` `core_deps_locked` retains `shinka-evolve` and adds `openhands-tools` as **sentinel keys** with `"v0.2-deferred-resolver"` / `"v0.2-deferred-license"` markers, so the pivot decision is not lost in cross-session progress files.

### Added
- `examples/01_hello_evolve.py` — 5-line demo runnable in <30s after `pip install darwinmcp` (architect-monitor recommendation).
- `tests/e2e/test_quickstart.py` — 30s budget gate around the demo (machine-enforced version of INV-10).
- `.darwinmcp-progress.json` committed at repo root with `current_step="P0-complete"` and the v0.1.0a1 verify results, so a next-session compact restore can pick up state from `git checkout` alone.

### Documented
- `R18_LICENSE_CHECK.md` § 1 now lists ISC (shellingham), PSF-2.0 (typing_extensions), and MPL-2.0 file-level-copyleft (certifi/tqdm) as permitted transitive deps with rationale.
- `lineage/circuitmap.py` docstring corrected — the previous wording said "the function raises on call" but the implementation returns an empty `CircuitMapAlpha`. The new wording matches the implementation.
- `bootstrap/honest_marketing.py` INV-2 grep is intentionally narrowed to **claim-shaped** numbers (`N.N%` etc.) rather than every decimal, to avoid false positives on version strings (`3.11`) and license identifiers ("Apache 2.0"). This is a deliberate spec narrowing of `project_evomcp_unified_synthesis_2026-05-24` § 7 INV-2 and is recorded here per the architect-monitor flag.

## [0.1.0a1] — 2026-05-24 (pre-alpha bootstrap)

### Added
- Phase 0 skeleton: package layout, deps pinned, license audit (`R18_LICENSE_CHECK.md`). `shinka-evolve` is **excluded** from v0.1 deps entirely — its PyPI release-cap (0.0.6) pins `httpx==0.27`, which conflicts with `mcp>=1.25`. The v0.1 mutator is `DummyLLM`; v0.2 will introduce a `[shinka-git]` extra using `git+https` against a compatible upstream commit.
- `evolve.llm.LLMBackend` ABC + `DummyLLM` (deterministic seed-diff backend, no network).
- `eval.fitness_base.FitnessTask` ABC + 1 sample `HelloWorldTask` (subprocess sandbox).
- `eval.sandbox_base.Sandbox` ABC + `SubprocessSandbox` (Python subprocess isolation, no docker dep in Phase 0).
- `seed/fs_tool/server.py` — single MCP seed server (the **only** structural placeholder in v0.1; explicitly marked).
- `lineage/graph.py` (networkx DAG) + `lineage/svg.py` (basic export). `lineage/circuitmap.py` = stub for Phase 2.
- `trace/tool_call_logger.py` — JSON dump of MCP tool calls per variant.
- `bootstrap/progress.py` — `.darwinmcp-progress.json` schema v2 read/write (compact-restore).
- `cli.py` — `darwinmcp` entry-point: `init` / `evolve` / `verify` / `version` subcommands.
- E2E smoke test (`tests/e2e/test_smoke.py`): DummyLLM × 1 generation × 1 HelloWorldTask in subprocess sandbox.
- Honest-marketing test (`tests/honest_marketing/test_readme_no_unmeasured_numbers.py`): regex-grep all DECIMALs in README and assert each is in the measured ledger or accompanied by `未測定`/`TBD`/`example`/`illustrative`.
- CI: ruff + pytest + INV-1 (no `NotImplementedError` outside `seed/fs_tool/`) + INV-2 (README numbers ledger) + INV-5 (`darwinmcp:main` entry-point exists) + INV-6 (license matrix == Apache/MIT/BSD/Python).

### Marketing honesty (per `feedback_ship-and-yank-lesson-2026-05-23`)
- **NO benchmark numbers in README** (no SWE-bench resolve rate, no tool-call success rate, no CircuitMap attribution score). These are explicitly marked **「未測定」** until Phase 1+ runs produce ledger entries.
- Sandbox is **subprocess-based, NOT docker-based** in v0.1 — escalation deferred to v0.2 (`openhands-tools` license + Python 3.12+ requirement triage).
- LLM backend is **DummyLLM (deterministic) by default** — `HFInferenceLLM` exists as stub only, full HF API integration is a v0.2 milestone.
- CircuitMap = **α 2-axis only** (lineage × tool-trace). The 3rd axis (cross-layer transcoder attribution) is a v0.2 milestone.
- This is pre-alpha. `pip install darwinmcp==0.1.0a1` runs the smoke test but does not produce publishable evolution metrics.

### Differentiation vs prior art (R18 — see `R18_LICENSE_CHECK.md` § 2)
- **`evolver` (EvoMap, GPL-3)** — prompt-only, no code mutation, no SWE-bench, no tool trace.
- **`OpenSpace` (HKUDS, MIT)** — skill-level evolution, MCP serving only (server.py unchanged), GDPVal benchmark.
- **`a-evolve` (A-EVO-Lab, MIT)** — workspace (prompts/skills/memory) mutation, SWE-bench claim but fitness internals undisclosed, no tool-trace lineage.

darwinmcp's residual niche: **MCP `server.py` code itself is mutated** + **SWE-bench Verified sandbox fitness** (Phase 1+) + **CircuitMap α 2-axis interpretability**.
