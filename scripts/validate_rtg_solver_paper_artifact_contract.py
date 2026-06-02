
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
def validate_artifact(artifact_path: Path, output_path: Path) -> Path:
    artifact = load_structured(artifact_path)
    fields = set(artifact.keys())
    has_boundary = "claim_boundary" in artifact or "presentation_claim_boundary" in artifact
    has_cost = "cost_model" in artifact or "executive_summary" in artifact or "results" in artifact
    has_status = "status" in artifact or "problem_statement" in artifact or "executive_summary" in artifact
    has_paper_shape = bool({"presentation_thesis", "abstract", "executive_summary", "results"} & fields)
    failures = []
    if not has_paper_shape:
        failures.append({"failure_type": "artifact_shape_not_recognized"})
    if not has_boundary:
        failures.append({"failure_type": "missing_claim_boundary"})
    if not has_cost:
        failures.append({"failure_type": "missing_cost_or_result_section"})
    if not has_status:
        failures.append({"failure_type": "missing_status_context"})
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "contract_surface": "rtg_solver_paper_artifact_contract",
        "artifact_contract_valid": not failures,
        "artifact_type": "solver_paper_or_report",
        "failures": failures,
        "observed_top_level_keys": sorted(fields),
        "summary": {"failure_count": len(failures), "contract_posture": "solver_paper_artifact_contract_valid" if not failures else "solver_paper_artifact_contract_review"},
        "receipt": {"artifact_sha256": sha256_file(artifact_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--artifact", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG solver paper artifact contract: " + str(validate_artifact(Path(a.artifact), Path(a.output))))
if __name__ == "__main__":
    main()
