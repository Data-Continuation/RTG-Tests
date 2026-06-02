#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OWNER = "GCAT-BCAT-Engine"
DEFAULT_REPO = "workflows"
DEFAULT_WORKFLOW = "math-solver.yml"
DEFAULT_REF = "main"

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path

def build_authority_request(manifest_path: Path, output_path: Path) -> Path:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    case_ids = [case.get("case_id", case.get("solver_case_id", "unknown")) for case in manifest.get("solver_cases", [])]
    request = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "authority_surface": "rtg_tv_tvc_authority_request",
        "authority_route": {
            "tv_repo": os.environ.get("RTG_TV_REPO", "StegVerse-Labs/TV"),
            "tvc_repo": os.environ.get("RTG_TVC_REPO", "StegVerse-Labs/TVC"),
            "authority_class": "math_solver_workflow_dispatch",
            "credential_boundary": "tv_tvc_brokered",
        },
        "target_workflow": {
            "owner": os.environ.get("RTG_MATH_SOLVER_OWNER", DEFAULT_OWNER),
            "repo": os.environ.get("RTG_MATH_SOLVER_REPO", DEFAULT_REPO),
            "workflow": os.environ.get("RTG_MATH_SOLVER_WORKFLOW", DEFAULT_WORKFLOW),
            "ref": os.environ.get("RTG_MATH_SOLVER_REF", DEFAULT_REF),
        },
        "solver_run_id": manifest.get("solver_run_id", "rtg-tv-tvc-solver-run"),
        "manifest_path": manifest_path.as_posix(),
        "manifest_sha256": sha256_file(manifest_path),
        "case_ids": case_ids,
        "case_count": len(case_ids),
        "requested_action": "authorize_math_solver_workflow_dispatch",
        "completion_rule": "do_not_dispatch_without_valid_tv_tvc_authority_receipt",
    }
    return write_json(output_path, request)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG TV/TVC authority request: " + str(build_authority_request(Path(a.manifest), Path(a.output))))

if __name__ == "__main__":
    main()
