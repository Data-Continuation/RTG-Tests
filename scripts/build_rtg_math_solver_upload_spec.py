
from __future__ import annotations
import json, hashlib, re
from datetime import datetime, timezone
from pathlib import Path

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_structured(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        data = {}
        cur = None
        for line in text.splitlines():
            if line and not line.startswith(" ") and ":" in line:
                k, v = line.split(":", 1)
                cur = k.strip()
                data[cur] = v.strip().strip("'\"") if v.strip() else []
            elif cur and line.strip().startswith("- "):
                if not isinstance(data[cur], list):
                    data[cur] = []
                data[cur].append(line.strip()[2:])
        return data

import argparse
def build_upload_spec(instruction_path: Path, output_path: Path) -> Path:
    instruction = load_structured(instruction_path)
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "upload_spec_surface": "rtg_math_solver_upload_spec_contract",
        "target_repo": instruction.get("target_solver_repo", "GCAT-BCAT-Engine/workflows"),
        "target_paths": {
            "problem_spec": "math_solver/validation/problem_spec_rtg_instruction.yml",
            "brain_reports": "math_solver/validation/brain_reports/",
            "candidate_vectors": "math_solver/validation/candidate_vectors/rtg/"
        },
        "workflow_targets": [".github/workflows/validation_run_inline.yml", ".github/workflows/validation_run.yml"],
        "workflow_inputs": {"run_id": instruction.get("formalism_state_id", "RTG-STATE-UNKNOWN"), "budget_ceiling": "10.00"},
        "expected_artifacts": ["real_results_<run_id>.json", "gcat_bcat_candidate_report.json", "gcat_bcat_candidate_summary.md", "publisher_document_or_solver_report.yml"],
        "semantic_boundary": instruction.get("claim_boundary", {}),
        "upload_spec_status": "ready_for_math_solver_upload_pattern",
        "receipt": {"instruction_sha256": sha256_file(instruction_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--instruction", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG math-solver upload spec: " + str(build_upload_spec(Path(a.instruction), Path(a.output))))
if __name__ == "__main__":
    main()
