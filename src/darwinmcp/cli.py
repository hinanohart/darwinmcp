"""darwinmcp command-line entry-point.

Subcommands:
  init      — write a fresh `.darwinmcp-progress.json` (schema v2) in $PWD.
  evolve    — run N generations using the chosen LLM backend (default: dummy).
  verify    — assert that every decimal number in README is in the measured ledger
              or accompanied by 未測定 / TBD / example / illustrative (INV-2).
  version   — print darwinmcp version.

Exit codes: 0 = OK, 2 = verify failure (CI ship-gate signal), 3 = smoke fail.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .bootstrap.progress import ProgressV2, read_progress, write_progress
from .eval.fitness_tasks import HelloWorldTask
from .eval.sandbox_subprocess import SubprocessSandbox
from .evolve.llm import get_backend
from .evolve.mutator import mutate
from .lineage.graph import LineageGraph
from .trace.tool_call_logger import ToolCallLogger


def _cmd_init(args: argparse.Namespace) -> int:
    cwd = Path.cwd()
    progress_path = cwd / ".darwinmcp-progress.json"
    if progress_path.exists() and not args.force:
        print(f"refusing to overwrite existing {progress_path} (use --force)", file=sys.stderr)
        return 1
    prog = ProgressV2.fresh(project_name=args.name or "darwinmcp")
    write_progress(progress_path, prog)
    print(f"wrote {progress_path}")
    return 0


def _cmd_evolve(args: argparse.Namespace) -> int:
    cwd = Path.cwd()
    progress_path = cwd / ".darwinmcp-progress.json"
    if not progress_path.exists():
        # auto-init for ergonomic first-run.
        prog = ProgressV2.fresh(project_name="darwinmcp")
        write_progress(progress_path, prog)
    else:
        prog = read_progress(progress_path)

    backend = get_backend(args.backend)
    task = HelloWorldTask()
    sandbox = SubprocessSandbox()
    lineage = LineageGraph()
    logger = ToolCallLogger()

    seed_path = Path(__file__).parent / "seed" / "fs_tool" / "server.py"
    seed_code = seed_path.read_text()
    parent_id = lineage.add_root(seed_code)

    for gen in range(args.generations):
        # Route every mutation through evolve.mutator.mutate — this is the
        # public surface that Phase-1 will swap to shinka-evolve-driven diffs.
        # Keeping cli.py thin around this call lets the loop stay stable.
        variant_code = mutate(seed_code, backend, generation=gen + 1, hint="add a comment")
        score = sandbox.run(task, variant_code, logger)
        child_id = lineage.add_child(parent_id, variant_code, fitness=score)
        prog.generation = gen + 1
        prog.fitness_tasks_count = max(prog.fitness_tasks_count, 1)
        prog.last_smoke_test_passed = score is not None and score >= 0
        write_progress(progress_path, prog)
        print(f"gen={gen + 1} variant={child_id} fitness={score}")
        seed_code = variant_code
        parent_id = child_id

    trace_path = cwd / "runs" / "trace.json"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    trace_path.write_text(json.dumps(logger.dump(), indent=2))
    print(f"wrote trace → {trace_path}")
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    repo_root = Path.cwd()
    readme = (repo_root / "README.md").read_text() if (repo_root / "README.md").exists() else ""
    ledger_path = repo_root / "docs" / "_ledger.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    from .bootstrap.honest_marketing import (
        check_readme_numbers,  # local import to avoid cli warmup cost
    )

    violations = check_readme_numbers(readme, ledger)
    if violations:
        for v in violations:
            print(f"INV-2 violation: {v}", file=sys.stderr)
        return 2
    print(
        "INV-2 OK: all README decimals are in ledger or accompanied by 未測定/TBD/example/illustrative."
    )
    return 0


def _cmd_version(_args: argparse.Namespace) -> int:
    print(__version__)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="darwinmcp", description="Evolve MCP server.py — pre-alpha")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="write a fresh .darwinmcp-progress.json")
    p_init.add_argument("name", nargs="?", default=None)
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(fn=_cmd_init)

    p_evolve = sub.add_parser("evolve", help="run N generations")
    p_evolve.add_argument("--generations", type=int, default=1)
    p_evolve.add_argument("--backend", default="dummy", choices=["dummy", "hf"])
    p_evolve.set_defaults(fn=_cmd_evolve)

    p_verify = sub.add_parser("verify", help="check README honest-marketing invariants")
    p_verify.set_defaults(fn=_cmd_verify)

    p_ver = sub.add_parser("version", help="print version")
    p_ver.set_defaults(fn=_cmd_version)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
