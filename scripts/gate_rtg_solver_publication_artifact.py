
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
def gate(contract_path: Path, claim_mapping_path: Path, cost_receipt_path: Path, output_path: Path) -> Path:
    contract = load_structured(contract_path)
    mapping = load_structured(claim_mapping_path)
    cost = load_structured(cost_receipt_path)
    failures = []
    if not contract.get("artifact_contract_valid"):
        failures.append("artifact_contract_invalid")
    if mapping.get("review_claims"):
        failures.append("claim_mapping_has_review_items")
    if not mapping.get("denied_claims"):
        failures.append("missing_denied_claims_boundary")
    if cost.get("max_observed_cost_usd") is None:
        failures.append("missing_cost_observation")
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "gate_surface": "rtg_solver_publication_artifact_gate",
        "publication_status": "publication_candidate_allowed_with_boundaries" if not failures else "publication_blocked_for_review",
        "failures": failures,
        "required_language": ["candidate generation", "human or formal verification required", "no autonomous theorem-proving claim unless independently verified"],
        "receipt": {"contract_sha256": sha256_file(contract_path), "claim_mapping_sha256": sha256_file(claim_mapping_path), "cost_receipt_sha256": sha256_file(cost_receipt_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--contract", required=True)
    p.add_argument("--claim-mapping", required=True)
    p.add_argument("--cost-receipt", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG solver publication artifact gate: " + str(gate(Path(a.contract), Path(a.claim_mapping), Path(a.cost_receipt), Path(a.output))))
if __name__ == "__main__":
    main()
