"""01_hello_evolve.py — runs a single DummyLLM generation, writes progress + trace.

Usage (after `pip install darwinmcp`):

    python examples/01_hello_evolve.py

Expected wall-clock: < 5 seconds on a developer laptop. The script exits with
code 0 iff the smoke generation completes and `.darwinmcp-progress.json`
reports `last_smoke_test_passed: true`.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from darwinmcp.cli import main


def run() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        import os

        cwd = os.getcwd()
        os.chdir(tmp)
        try:
            if main(["init"]) != 0:
                return 1
            if main(["evolve", "--generations", "1", "--backend", "dummy"]) != 0:
                return 1
            raw = json.loads(Path(".darwinmcp-progress.json").read_text())
            if not raw.get("last_smoke_test_passed"):
                print("smoke did NOT pass", file=sys.stderr)
                return 1
            print(f"OK — generation={raw['generation']}, smoke passed.")
            return 0
        finally:
            os.chdir(cwd)


if __name__ == "__main__":
    raise SystemExit(run())
