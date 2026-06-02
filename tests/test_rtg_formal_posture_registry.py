#!/usr/bin/env python3
"""RTG formal posture registry layer tests."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "register_rtg_formal_postures.py"
SCHEMA = ROOT / "schemas" / "rtg_formal_posture_registry.schema.json"
TMP = ROOT / "build" / "formal-posture-registry-test"
INPUT_DIR = TMP / "input"
OUTPUT = TMP / "rtg_formal_posture_registry.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def write_posture(path: Path, run_id: str, posture: str, case_count: int) -> None:
    payload = {
        "schema_version": "1.0",
        "generated": "2026-01-01T00:00:00Z",
        "source_repo": "Data-Continuation/RTG-Tests",
        "solver_run_id": run_id,
        "source_solver_results": f"build/solver-results/{run_id}/solver_results.json",
        "formal_posture": posture,
        "case_postures": [
            {
                "case_id": f"{run_id}-CASE-{idx:03d}",
                "solver_posture": "satisfiable",
                "rtg_admissibility": "admissible",
            }
            for idx in range(1, case_count + 1)
        ],
        "admissibility_summary": {
            "case_count": case_count,
            "solver_posture_counts": {"satisfiable": case_count},
            "rtg_admissibility_counts": {"admissible": case_count},
        },
        "receipt": {
            "solver_results_sha256": "0" * 64,
            "ingestion_surface": "rtg_solver_result_ingestion",
            "target_workflow_reference": "GCAT-BCAT-Engine/workflows/math-solver",
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    require(SCRIPT.exists(), "formal posture registry script is missing")
    require(SCHEMA.exists(), "formal posture registry schema is missing")

    if TMP.exists():
        shutil.rmtree(TMP)

    write_posture(INPUT_DIR / "run-a" / "rtg_formal_posture.json", "run-a", "formally_consistent", 2)
    write_posture(INPUT_DIR / "run-b" / "rtg_formal_posture.json", "run-b", "underconstrained", 1)

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--input-dir", str(INPUT_DIR), "--output", str(OUTPUT)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)

    require(OUTPUT.exists(), "formal posture registry was not written")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    registry = json.loads(OUTPUT.read_text(encoding="utf-8"))

    missing = set(schema["required"]) - set(registry)
    require(not missing, "formal posture registry missing required fields: " + repr(sorted(missing)))

    require(registry["schema_version"] == "1.0", "schema_version mismatch")
    require(registry["source_repo"] == "Data-Continuation/RTG-Tests", "source_repo mismatch")
    require(registry["registry_type"] == "rtg_formal_posture_registry", "registry_type mismatch")
    require(registry["summary"]["record_count"] == 2, "record_count mismatch")
    require(registry["summary"]["total_case_count"] == 3, "total_case_count mismatch")
    require(registry["summary"]["formal_posture_counts"]["formally_consistent"] == 1, "consistent count mismatch")
    require(registry["summary"]["formal_posture_counts"]["underconstrained"] == 1, "underconstrained count mismatch")
    require(registry["summary"]["ready_for_formal_claim_count"] == 1, "ready count mismatch")
    require(registry["summary"]["review_required_count"] == 1, "review count mismatch")
    require(len(registry["receipt"]["record_hashes"]) == 2, "record hash count mismatch")

    print("RTG formal posture registry tests passed.")


if __name__ == "__main__":
    main()
