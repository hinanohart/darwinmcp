# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0a3] — 2026-05-24 (meta-audit hotfix; 4-agent re-review)

A second 3-agent + 1-critic meta-audit was run after v0.1.0a2. The 3 prior monitors (B1/B2/M) had returned unanimous SHIP-OK but shared a structural blind spot — they only verified *internal* coherence (code ⇄ memory spec) and never validated the repo ⇄ external-world boundary (PyPI / git URL). The meta-audit found 2 FATAL, 10 HIGH, 11 MED, all bundled here.

### Fixed (FATAL)
- README install command was `pip install darwinmcp==0.1.0a1` while `__version__ == 0.1.0a2`. Rewritten to `pip install "git+https://github.com/hinanohart/darwinmcp@v0.1.0a3"` and PyPI publish honestly deferred to v0.1.0 GA.
- `pip install darwinmcp` (PyPI) was instructed despite the package not existing on PyPI (`https://pypi.org/pypi/darwinmcp/json` → 404). The git+https form above resolves this.

### Fixed (HIGH)
- `cli.py::_cmd_verify` read the ledger as `{"_comment":…, "version":…, "measurements":…}` raw, while the honest-marketing test correctly unwrapped `["measurements"]`. The CLI now matches CI — `darwinmcp verify` will accept a populated ledger.
- `eval/fitness_tasks.py::HelloWorldTask.probe` used manual `\\"\\"\\"` / `\\'` escaping that silently mis-scored variants ending in a backslash. Rewritten to `repr(variant_code)` round-trip — no escape arithmetic.
- README "only structural placeholder" wording reworded to "only *run-path* placeholder", with `evolve/llm.py::HFInferenceLLM` explicitly named as the second allowed (construction-time) NotImplementedError site. Matches the CI grep allowlist and INV-1 test.
- `bootstrap/honest_marketing.py` INV-2 regex hardened: now matches both number-then-unit AND unit-then-number forms, plus a new `_CLAIM_RE_UNIT_NUM` for "Score: 76.8" / "accuracy 76.8" patterns. 12 fuzz cases added in `tests/honest_marketing/test_inv2_regex_fuzz.py`.
- `mcp_compat.assert_compatible` was dead code (no caller in src/ or tests/). Now wired into `cli.py::main` for the `evolve` subcommand only (so `version` / `init` / `verify` remain usable when `mcp` is absent).
- `evolve/llm.py::HFInferenceLLM.__init__` dropped the dead `_ = os.environ.get("HF_TOKEN")` read.
- `release.yml` now machine-enforces **INV-7** (tag ↔ `current_step` sync — the saelet failure mode) and **INV-11** (3-agent verify gate, GA-only — guarded by `!contains(ref_name, 'a/b/rc')`).
- `ci.yml` adds **INV-12** (README install command ↔ `__version__` consistency check) — would have caught the FATAL above before tag time.
- README adds an honest "Dependency disclosure" paragraph: v0.1 imports only `networkx` + `importlib.metadata`; `mcp`/`huggingface-hub`/`pydantic`/`rich` are forward-compat pins (and capped `<2` where not already capped).

### Fixed (MED)
- `bootstrap/progress.py` now validates `$schema_version` on read (loud failure on v0.1↔v0.2 mismatch instead of silent `TypeError`).
- `bootstrap/progress.py::write_progress` is now atomic (`tempfile`-style `replace`) per the original spec.
- `lineage/circuitmap.py::CircuitMapAlpha` gains `measured: bool = False` so Phase-2 non-empty `cells` cannot land without flipping the flag (spec INV-6).
- `eval/sandbox_subprocess.py` adds `RLIMIT_AS` (256 MiB) via `preexec_fn` on Linux, graceful no-op elsewhere.
- README "always passes in pre-alpha" softened to "currently passes while the ledger is empty" (per `feedback_no-permanent-claim-2026-05-14`).
- `pyproject.toml` keyword `"swe-bench"` → `"swe-bench-roadmap"` so a PyPI searcher landing from a SWE-bench query is not misled.
- `pyproject.toml` upper bounds added: `huggingface-hub<2`, `pydantic<3` (mcp already `<2`).
- `release.yml` smoke step extended: `darwinmcp init && darwinmcp evolve --generations 1 --backend dummy` (not just `darwinmcp version`) — verifies the install actually runs.
- `ci.yml` matrix gains Python 3.13.
- New: `tests/integration/test_fitness_monotonic.py` (skip-marked stub, locks INV-3 slot for Phase 1).
- New: `tests/unit/test_lineage_merkle.py` (xfail-marked, locks INV-4 parent-hash requirement).
- New: `tests/honest_marketing/test_forbidden_until_measured.py` (forbidden_until_measured guard — honest marketing) — fails if `swe_bench_resolve_rate` / `tool_call_success_rate` / `circuitmap_attribution_score` appear in README/CHANGELOG outside an allow-context token.

### Documented
- All B1/B2/M v0.1.0a2 verdicts confirmed unchanged; the meta-audit findings are additive, not corrective. 3-monitor template is now augmented with a 4th axis: **W (world-checker)** — verifies repo ⇄ external world (PyPI, git URL, README install command resolvability). To be applied at every future ship gate.

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
- This is pre-alpha. `pip install "git+https://github.com/hinanohart/darwinmcp@v0.1.0a3"` runs the smoke test but does not produce publishable evolution metrics.

### Differentiation vs prior art (R18 — see `R18_LICENSE_CHECK.md` § 2)
- **`evolver` (EvoMap, GPL-3)** — prompt-only, no code mutation, no SWE-bench, no tool trace.
- **`OpenSpace` (HKUDS, MIT)** — skill-level evolution, MCP serving only (server.py unchanged), GDPVal benchmark.
- **`a-evolve` (A-EVO-Lab, MIT)** — workspace (prompts/skills/memory) mutation, SWE-bench claim but fitness internals undisclosed, no tool-trace lineage.

darwinmcp's residual niche: **MCP `server.py` code itself is mutated** + **SWE-bench Verified sandbox fitness** (Phase 1+) + **CircuitMap α 2-axis interpretability**.
