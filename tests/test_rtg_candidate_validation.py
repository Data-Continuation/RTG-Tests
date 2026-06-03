#!/usr/bin/env python3
"""Declared-task wrapper: run the RTG governance validator over RTG candidate
vectors and fail (non-zero) unless all candidate postures match expected.

Kept to the repo's 2-element command convention
(["python", "tests/<file>.py"]) by hard-coding repo-relative paths here
rather than passing CLI flags through the dispatcher registry.

This is the RTG-side parity counterpart to the GCAT/BCAT candidate
validation workflow: same posture surface (ALLOW/DENY/DEFER/REPLAY),
same all-pass gate, repo-local-only.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "math-solver" / "validation" / "rtg_candidate_validator.py"
VECTORS = ROOT / "math-solver" / "validation" / "candidate_vectors" / "rtg"
OUT = ROOT / "math-solver" / "validation" / "rtg_candidate_report.json"
SUMMARY = ROOT / "math-solver" / "validation" / "rtg_candidate_summary.md"


def main() -> int:
    if not VALIDATOR.exists():
        print(f"RTG validator missing: {VALIDATOR.relative_to(ROOT)}")
        return 1
    if not VECTORS.exists():
        print(f"RTG vectors missing: {VECTORS.relative_to(ROOT)}")
        return 1
    result = subprocess.run(
        [sys.executable, str(VALIDATOR),
         "--vectors", str(VECTORS),
         "--out", str(OUT),
         "--summary-md", str(SUMMARY)],
        cwd=ROOT, text=True,
    )
    if result.returncode != 0:
        print("RTG candidate validation FAILED (not all postures matched expected).")
        return result.returncode
    print("RTG candidate validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
