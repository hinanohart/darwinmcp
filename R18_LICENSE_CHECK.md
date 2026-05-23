# R18 License & Prior-Art Audit — darwinmcp v0.1

> Performed: 2026-05-24 (Phase 0, pre `gh repo create`).
> Auditor: hinanohart (automated, 3 WebFetch + 5 WebSearch).
> Policy: dependencies licensed Apache-2.0 / MIT / BSD-3 / Python-2.0 only. Anything else → exclude or reference-only.

---

## § 1. Dependency License Matrix

| Package | Pin | License | Source-verified | Distributed in wheel? |
|---|---|---|---|---|
| `mcp` | `>=1.25,<2` | MIT | https://pypi.org/project/mcp/ (v1.27.1, 2026-05-08) | No (runtime dep) |
| `huggingface-hub` | `>=0.24` | Apache-2.0 | https://pypi.org/project/huggingface-hub/ | No |
| `pydantic` | `>=2.5` | MIT | https://pypi.org/project/pydantic/ | No |
| `networkx` | `>=3.2` | BSD-3-Clause | https://pypi.org/project/networkx/ | No |
| `rich` | `>=13` | MIT | https://pypi.org/project/rich/ | No |

### Excluded (license- or resolver-risk in v0.1 — deferred to v0.2)
| Package | Reason |
|---|---|
| `shinka-evolve` | LICENSE is Apache-2.0 ✓ (direct read, 2026-05-24). **Excluded for a resolver reason, not a license reason**: PyPI release-cap at 0.0.6 pins `httpx==0.27`, conflicting with `mcp>=1.25` which requires `httpx>=0.27.1`. The v0.1 mutator uses `DummyLLM` only (no shinka import). v0.2 will integrate via `pip install darwinmcp[shinka-git]` using `git+https` against a compatible upstream commit. |
| `openhands-tools` | License **not stated** on PyPI page (2026-05-24 check). Python ≥3.12 requirement. **Replaced by in-tree `eval.sandbox_subprocess.SubprocessSandbox`** in Phase 0. |
| `dspy-ai` | Not needed in Phase 0; Phase 2 candidate (license check at that time). |
| `swe-bench` | Patches in repo are not redistributable (license per-task); Phase 1+ uses URL reference + on-demand fetch, **patches are NOT bundled in the wheel**. |
| Llama-derived weights | Llama Community License = evaluation-only, NOT distributed; reference in docs only. |
| Codestral / Mistral-NPL | Excluded entirely (NPL forbids many commercial uses). |
| Gemma 2 / Gemma 3 | ToU (not OSI-approved). Gemma 4 (Apache-2.0, 2026-04~) is acceptable if used; not in Phase 0. |
| CC-BY-NC datasets | Research-only; not bundled. |

### CI enforcement
`.github/workflows/ci.yml` runs `pip-licenses --format=csv --fail-on="GPL;LGPL;AGPL;NPL;ToU;Proprietary;UNKNOWN"` against the resolved env. A non-Apache/MIT/BSD/Python dep failing this check → CI red → release blocked (INV-6).

---

## § 2. Prior-Art Audit (3 WebFetch + 5 WebSearch, 2026-05-24)

R14 探索の R18 段階で「evolvable MCP server」相当の prior art を網羅確認。元名称 `EvoMCP` は generic すぎ + `mcp-forge` も検索性衝突 → `darwinmcp` に rename。

### § 2.1 Detected prior art

| Project | License | Scope (what it does) | Overlap with darwinmcp's claim |
|---|---|---|---|
| [EvoMap/evolver](https://github.com/EvoMap/evolver) + `gep-mcp-server` | **GPL-3.0** ⚠ | Prompt-generation engine. Tracks Genes/Capsules/Events as audit trail. **Does NOT auto-edit source code.** | Partial (MCP + evolve naming). **GPL-3 forbids code copy** — reference only, no borrow. |
| [HKUDS/OpenSpace](https://github.com/HKUDS/OpenSpace) | MIT | Self-evolving *skill* system. Diff-based patches on skills (not server.py). GDPVal benchmark. Version DAG over skills. | Partial (skill genealogy ≠ server.py mutation, GDPVal ≠ SWE-bench, no tool-trace). |
| [A-EVO-Lab/a-evolve](https://github.com/A-EVO-Lab/a-evolve) | MIT | 5-phase (Solve→Observe→Evolve→Gate→Reload) workspace mutation. MCP seed workspace included. SWE-bench 76.8% (fitness internals undisclosed). | Partial (workspace mutation ≠ server.py mutation, no tool-trace lineage). |
| [iddv/mcp-forge](https://github.com/iddv/mcp-forge) + [KennyVaneetvelde/mcp-forge](https://github.com/KennyVaneetvelde/mcp-forge) | (varies) | MCP server **scaffolding/boilerplate generator**. | Naming overlap only — scope unrelated. (Reason `mcpforge` was rejected as darwinmcp's name.) |
| [IBM/mcp-context-forge](https://github.com/IBM/mcp-context-forge) | (Apache-2.0 likely) | AI gateway/proxy in front of MCP. | Naming overlap only — scope unrelated. |

### § 2.2 Residual niche (darwinmcp's 3 differentiation axes)

All three are absent in **every** prior-art project above:

1. **MCP `server.py` code itself is mutated** across generations — not skills, not prompts, not workspace files.
2. **SWE-bench Verified Sandbox real-execution fitness** (Phase 1+, fixed task subset, fully reproducible).
3. **CircuitMap α 2-axis interpretability** = lineage graph × tool-call trace cross-attribution (Phase 2; the 3rd axis, cross-layer transcoder attribution, is v0.2 backlog).

Moat estimate: **3.0 / 5** (down from synthesis's 3.2 due to prior-art exposure, but the 3 axes are clean).

### § 2.3 Overturn-conditions (auto-stop triggers per `feedback_phase0_sae_mcp_overturned_2026-05-23`)
If any of the following is detected in Phase 0–4, **HALT auto-progression** and revert:
1. A new prior-art project that mutates MCP `server.py` code + uses SWE-bench Verified + provides tool-trace lineage (all three axes).
2. MCP spec 2026-07-28 RC ("Tasks/Apps") absorbs `server.py` evolution as a first-class concern.
3. `shinka-evolve` upstream relicenses (away from Apache-2.0). Note: PyPI distribution-cap (0.0.6) is **not** an overturn — we already moved it to the `[shinka]` opt-in extra in v0.1 and target the GitHub release in v0.2.

---

## § 3. Distribution form (wheel content)

The published `darwinmcp` wheel contains **only** `src/darwinmcp/**/*.py` + `LICENSE` + `NOTICE` + `README.md`. It does **NOT** bundle:
- `shinka-evolve` source (opt-in `[shinka]` extra, pip-installed by user; not in default install)
- SWE-bench task patches (URL reference, runtime fetch — Phase 1+)
- HuggingFace model weights (runtime fetch via `huggingface-hub`)
- `seed/fs_tool/server.py` patches from third parties

All bundled files are 100% authored in this repo under Apache-2.0.

---

## § 4. Signatures

- ShinkaEvolve LICENSE direct-read: confirmed `Apache License Version 2.0, January 2004` as the first line of the file (2026-05-24).
- `mcp` PyPI page MIT confirmed (2026-05-24).
- `openhands-tools` LICENSE absence noted, dep removed from Phase 0.
- Prior-art audit conducted via WebFetch on the three GitHub repos listed in § 2.1.

— end of R18 audit —
