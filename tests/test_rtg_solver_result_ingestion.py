#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ingest_rtg_solver_results.py"
SCHEMA = ROOT / "schemas" / "rtg_formal_posture.schema.json"
TMP = ROOT / "build" / "solver-result-ingestion-test"
INPUT = TMP / "solver_results.json"
OUTPUT = TMP / "rtg_formal_posture.json"

def require(ok, msg):
    if not ok:
        raise AssertionError(msg)

def main():
    require(SCRIPT.exists(), "solver result ingestion script is missing")
    require(SCHEMA.exists(), "formal posture schema is missing")
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)
    INPUT.write_text(json.dumps({
        "schema_version": "1.0",
        "source_repo": "Data-Continuation/RTG-Tests",
        "target_workflow_reference": "GCAT-BCAT-Engine/workflows/math-solver",
        "solver_run_id": "rtg-solver-run-test-001",
        "case_results": [
            {"case_id":"ADAPTER-SAMPLE-001","solver_posture":"satisfiable","solver_confidence":0.99},
            {"case_id":"ADAPTER-SAMPLE-002","solver_posture":"equivalent_to_prior_case","solver_confidence":0.91}
        ]
    }, indent=2) + "\n", encoding="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPT), "--input", str(INPUT), "--output", str(OUTPUT)], cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    require(OUTPUT.exists(), "formal posture output was not written")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    record = json.loads(OUTPUT.read_text(encoding="utf-8"))
    missing = set(schema["required"]) - set(record)
    require(not missing, "missing required fields: " + repr(sorted(missing)))
    require(record["schema_version"] == "1.0", "schema_version mismatch")
    require(record["formal_posture"] == "formally_consistent", "formal_posture mismatch")
    require(record["admissibility_summary"]["case_count"] == 2, "case_count mismatch")
    require(record["admissibility_summary"]["rtg_admissibility_counts"]["admissible"] == 1, "admissible count mismatch")
    require(record["admissibility_summary"]["rtg_admissibility_counts"]["admissible_equivalent"] == 1, "equivalent count mismatch")
    require("solver_results_sha256" in record["receipt"], "receipt missing hash")
    print("RTG solver result ingestion tests passed.")

if __name__ == "__main__":
    main()
