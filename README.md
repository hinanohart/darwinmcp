# darwinmcp

> **Pre-alpha.** Evolve an MCP server's `server.py` code across generations using sandbox-executed fitness and lineage × tool-trace interpretability. **No benchmark numbers are advertised in this README** — see [Honest Marketing](#honest-marketing).

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Status: Pre-alpha](https://img.shields.io/badge/status-pre--alpha-orange)](#current-status)
[![Python: 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)

## What it is

`darwinmcp` is a small framework that **mutates an MCP server's `server.py` file across generations**, scores each variant by running it in a subprocess sandbox against task probes, and writes the per-generation lineage + per-tool-call trace to disk for later inspection.

This is **not** a benchmark harness, a model trainer, or an agent runtime. It is a thin loop on top of:

- [`mcp`](https://pypi.org/project/mcp/) — MIT, the official Model Context Protocol Python SDK
- [`networkx`](https://pypi.org/project/networkx/) — BSD-3, lineage DAG
- Built-in `subprocess` — sandbox (docker-based runtimes deferred to v0.2)
- [`shinka-evolve`](https://github.com/SakanaAI/ShinkaEvolve) (Apache-2.0) — LLM-guided code mutation. **Not used in v0.1** (PyPI release-cap conflicts with `mcp>=1.25`; see [`R18_LICENSE_CHECK.md`](R18_LICENSE_CHECK.md) § 1). v0.2 integrates via a `git+https` extra (`darwinmcp[shinka-git]`). The v0.1 mutator is `DummyLLM`.

## Differentiation vs prior art (R18 audit)

`darwinmcp` targets a niche the following existing projects do **not** cover (see [`R18_LICENSE_CHECK.md`](R18_LICENSE_CHECK.md) § 2 for the full audit):

| Project | What it does | What it doesn't do |
|---|---|---|
| `EvoMap/evolver` (GPL-3) | prompt evolution, audit trail | does NOT mutate source code; no MCP server.py target |
| `HKUDS/OpenSpace` (MIT) | skill evolution, MCP serving | server.py is unchanged; no tool-trace lineage |
| `A-EVO-Lab/a-evolve` (MIT) | workspace (prompts/skills/memory) mutation | server.py mutation, fitness internals, and tool-trace lineage not exposed |

`darwinmcp`'s residual niche is the combination of three axes:
1. The MCP `server.py` file itself is the mutation target.
2. Fitness comes from a real subprocess (v0.1) / SWE-bench Verified (v0.2+) sandbox.
3. Lineage × tool-call-trace 2-axis interpretability (CircuitMap α). The 3rd axis (cross-layer transcoder attribution) is v0.2 backlog.

## Install

```bash
pip install darwinmcp==0.1.0a1
# or
uv pip install darwinmcp==0.1.0a1
```

Requires Python 3.11+.

## Quickstart

```bash
darwinmcp init my-run           # writes .darwinmcp-progress.json in $PWD
darwinmcp evolve --generations 1 --backend dummy   # 1 generation, deterministic
darwinmcp verify                # asserts ledger ⊇ README numbers (always passes in pre-alpha — no numbers asserted)
```

The `dummy` backend produces deterministic diffs without any network call. The `hf` backend (HuggingFace Inference API, default model `Qwen/Qwen2.5-Coder-32B-Instruct`) is implemented as a stub in v0.1 and fully wired in v0.2.

## Current status

- **v0.1.0a1 (this release)** — Phase 0 bootstrap. Skeleton, ABCs, dummy LLM, subprocess sandbox, 1 sample task (`HelloWorldTask`), lineage stub, CI honesty enforcement. **All metric placeholders read 未測定.**
- **v0.1.0** — Phase 1+2 + 3-agent ship verify gate. ETA: 6 weeks from 2026-05-24 per `project_evomcp_unified_synthesis_2026-05-24.md`.
- **v0.2** — HF backend live, docker sandbox option, SWE-bench Verified fitness adapter, CircuitMap α 3rd axis.

## Honest Marketing

This project follows `feedback_ship-and-yank-lesson-2026-05-23`:

- **No claimed benchmark numbers** appear in this README. Any number that does appear must be either (a) in the measured ledger `docs/_ledger.json` or (b) followed by `未測定` / `TBD` / `example` / `illustrative` in the same paragraph. CI enforces this via `tests/honest_marketing/test_readme_no_unmeasured_numbers.py`.
- **No CI grep whitelist.** Numbers are not exempted by name.
- **The only structural placeholder** in the v0.1 package is `src/darwinmcp/seed/fs_tool/server.py`, which is the *target of mutation* and is explicitly marked. Everywhere else, `NotImplementedError` is forbidden (CI INV-1).
- **`pip install` runs the smoke test.** If the entry-point `darwinmcp` is missing or broken, CI fails (INV-5).
- **Vendor checkmarks** (e.g. "✓ uses X") link to that vendor's actual public statement, not to an aspirational claim.

## License

[Apache-2.0](LICENSE) © 2026 hinanohart. See [`NOTICE`](NOTICE) for third-party attributions, [`R18_LICENSE_CHECK.md`](R18_LICENSE_CHECK.md) for the full license & prior-art audit.

## Contributing

Pre-alpha. Issues welcome; PRs gated on (a) license check (Apache/MIT/BSD/Python only for deps) and (b) the 3-agent verify gate at v0.1.0 ship (see `project_evomcp_unified_synthesis_2026-05-24.md` for the 11 invariants).
