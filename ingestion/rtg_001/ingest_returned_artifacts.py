#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "fixtures" / "returned_artifacts" / "rtg_001"
OUT = ROOT / "ingestion" / "rtg_001" / "rtg_001_ingestion_result.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    policy = read_json(ROOT / "config" / "rtg_001_ingestion_policy.json")
    artifacts = {name: read_json(FIXTURES / name) for name in policy["required_artifacts"]}
    report = artifacts["ext2_report.json"]

    for field in policy["required_report_fields"]:
        require(field in report, f"Report missing field: {field}")

    require(report["run_id"] == policy["run_id"], "Run ID mismatch")
    require(isinstance(report["total_cost"], (int, float)), "Total cost must be numeric")
    require(report["total_cost"] >= 0, "Total cost cannot be negative")
    require(isinstance(report["total_tokens"], int), "Total tokens must be integer")
    require(report["total_tokens"] > 0, "Total tokens must be positive")
    require(report["sources_verified"] is True, "Sources must be verified before ingestion")

    for key, expected in policy["claim_boundary_requirements"].items():
        require(report["claim_boundary"].get(key) is expected, f"Claim boundary mismatch for {key}")

    require(artifacts["ext2_phase1.json"]["phase"] == 1, "Phase 1 artifact invalid")
    require(artifacts["ext2_sources.json"]["phase"] == 2, "Source artifact invalid")
    require(artifacts["ext2_phase3.json"]["phase"] == 3, "Phase 3 artifact invalid")

    result = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "run_id": report["run_id"],
        "source_repo": policy["source_repo"],
        "execution_repo": policy["execution_repo"],
        "ingestion_status": "complete",
        "from_state": policy["state_transition"]["from"],
        "to_state": policy["state_transition"]["to"],
        "next_state": policy["post_ingestion_next_state"],
        "cost_receipt": {
            "total_cost": report["total_cost"],
            "total_tokens": report["total_tokens"],
            "pre_execution_estimate_replaced_by_receipt": True
        },
        "claim_boundary_preserved": True,
        "sources_verified": True,
        "artifacts_ingested": policy["required_artifacts"],
        "false_claims_blocked": {
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("RTG-001 returned artifact ingestion module passed.")


if __name__ == "__main__":
    main()
