
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
def map_claims(artifact_path: Path, contract_path: Path, output_path: Path) -> Path:
    artifact = load_structured(artifact_path)
    contract = load_structured(contract_path)
    boundary = artifact.get("claim_boundary", {})
    allowed, denied = [], []
    if isinstance(boundary, dict):
        for k in ("what_this_framework_proves", "what_this_paper_proves", "what_this_artifact_proves"):
            v = boundary.get(k, [])
            allowed.extend(v if isinstance(v, list) else [v])
        for k in ("what_this_framework_does_not_claim", "what_this_paper_does_not_claim", "what_this_artifact_does_not_claim"):
            v = boundary.get(k, [])
            denied.extend(v if isinstance(v, list) else [v])
    if not allowed and artifact.get("presentation_claim"):
        allowed.append(artifact["presentation_claim"])
    if not denied:
        denied.append("Autonomous theorem proving is not claimed without human or formal verification.")
    review = [] if contract.get("artifact_contract_valid") else ["Artifact contract invalid; claims require review."]
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "mapping_surface": "rtg_solver_claim_boundary_mapping",
        "allowed_claims": allowed,
        "denied_claims": denied,
        "review_claims": review,
        "claim_boundary_status": "mapped_with_boundaries" if not review else "mapped_with_review_required",
        "receipt": {"artifact_sha256": sha256_file(artifact_path), "contract_sha256": sha256_file(contract_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--artifact", required=True)
    p.add_argument("--contract", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG solver claim boundary mapping: " + str(map_claims(Path(a.artifact), Path(a.contract), Path(a.output))))
if __name__ == "__main__":
    main()
