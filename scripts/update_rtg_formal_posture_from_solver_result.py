#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path

def classify_overall(postures: list[str]) -> str:
    if any(p in {"formally_contradictory", "contradictory"} for p in postures):
        return "formal_posture_contradiction_detected"
    if any(p in {"underconstrained", "requires_new_axiom", "requires_new_operator"} for p in postures):
        return "formal_posture_requires_expansion"
    if postures and all(p in {"formally_consistent", "satisfiable"} for p in postures):
        return "formal_posture_consistent_candidate"
    return "formal_posture_review"

def update_posture(bridge_path: Path, output_path: Path) -> Path:
    bridge = json.loads(bridge_path.read_text(encoding="utf-8"))
    bridged_results = bridge.get("bridged_results", [])
    postures = [item.get("formal_posture", "") for item in bridged_results]
    overall = classify_overall(postures)
    record = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "posture_surface": "rtg_formal_posture_update_from_solver_result",
        "solver_run_id": bridge.get("solver_run_id"),
        "formal_posture_status": overall,
        "case_postures": [
            {
                "case_id": item.get("case_id"),
                "solver_status": item.get("solver_status"),
                "formal_posture": item.get("formal_posture"),
            }
            for item in bridged_results
        ],
        "next_governance_target": "formal_posture_registry",
        "summary": {
            "case_posture_count": len(bridged_results),
            "formal_posture_status": overall,
        },
        "receipt": {
            "ingestion_bridge_sha256": sha256_file(bridge_path),
        },
    }
    return write_json(output_path, record)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--bridge", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG formal posture update from solver result: " + str(update_posture(Path(a.bridge), Path(a.output))))

if __name__ == "__main__":
    main()
