#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

WORKFLOW_REFERENCE = "GCAT-BCAT-Engine/workflows/math-solver"

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build_packet(manifest_path: Path, output_path: Path, workflow_reference: str = WORKFLOW_REFERENCE) -> Path:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    case_ids = [case.get("case_id", case.get("solver_case_id", "unknown")) for case in manifest.get("solver_cases", [])]
    packet = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "dispatch_surface": "rtg_actual_math_solver_dispatch",
        "target_workflow_reference": workflow_reference,
        "dispatch_status": "dispatch_ready",
        "solver_run_id": manifest.get("solver_run_id", "rtg-solver-run-unknown"),
        "input_manifest_path": manifest_path.as_posix(),
        "input_manifest_sha256": sha256_file(manifest_path),
        "case_ids": case_ids,
        "case_count": len(case_ids),
        "expected_solver_result_path": "build/solver-results/solver_results.json",
        "completion_rule": "do_not_mark_complete_until_solver_results_json_exists",
        "receipt": {
            "dispatch_packet_surface": "rtg_actual_math_solver_dispatch",
            "source_manifest_sha256": sha256_file(manifest_path),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--workflow-reference", default=WORKFLOW_REFERENCE)
    a = p.parse_args()
    print("Wrote RTG math-solver dispatch packet: " + str(build_packet(Path(a.manifest), Path(a.output), a.workflow_reference)))

if __name__ == "__main__":
    main()
