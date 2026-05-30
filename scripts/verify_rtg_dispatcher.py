#!/usr/bin/env python3
"""Verify the RTG repo dispatcher contract.

This is a smoke-level contract test. It verifies that:
- declared tasks can be loaded;
- dry-run dispatch works;
- unknown task names are rejected.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPATCHER = ROOT / "scripts" / "rtg_dispatcher.py"


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DISPATCHER), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def main() -> None:
    list_result = run_command(["--list"])
    if list_result.returncode != 0:
        raise SystemExit(list_result.stderr or list_result.stdout)

    if "fixture_smoke_tests" not in list_result.stdout:
        raise SystemExit("Missing declared task: fixture_smoke_tests")

    dry_run_result = run_command(["--task", "all", "--dry-run"])
    if dry_run_result.returncode != 0:
        raise SystemExit(dry_run_result.stderr or dry_run_result.stdout)

    if "dry_run: true" not in dry_run_result.stdout:
        raise SystemExit("Dispatcher dry-run did not report dry_run: true")

    unknown_result = run_command(["--task", "not_declared"])
    if unknown_result.returncode == 0:
        raise SystemExit("Dispatcher accepted an undeclared task.")

    if "Unknown task" not in (unknown_result.stderr + unknown_result.stdout):
        raise SystemExit("Unknown-task rejection did not include expected message.")

    print("RTG dispatcher contract verified.")


if __name__ == "__main__":
    main()
