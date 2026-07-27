#!/usr/bin/env python3
"""Validate bounded Transition Table results returned to RTG."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUEST_PATH = ROOT / "fixtures" / "rtg-tt-request.example.json"
RESULT_PATH = ROOT / "fixtures" / "rtg-tt-result.example.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_hash(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def correlate(request: dict, result: dict) -> list[str]:
    errors: list[str] = []
    if result.get("contract_version") != request.get("contract_version"):
        errors.append("contract_version_mismatch")
    if result.get("request_id") != request.get("request_id"):
        errors.append("request_id_mismatch")
    if result.get("candidate_transition_id") != request.get("candidate_transition_id"):
        errors.append("candidate_transition_id_mismatch")
    if not set(result.get("authority_refs_evaluated", [])).issubset(set(request.get("authority_refs", []))):
        errors.append("unknown_authority_ref")
    if not set(result.get("evidence_refs_evaluated", [])).issubset(set(request.get("evidence_refs", []))):
        errors.append("unknown_evidence_ref")
    if result.get("execution_authorized") and not result.get("commit_authorized"):
        errors.append("execution_without_commit")
    if result.get("resolution") == "DENY" and (
        result.get("commit_authorized") or result.get("execution_authorized")
    ):
        errors.append("deny_with_authorization")
    if result.get("resolution") == "ALLOW" and result.get("admissibility") != "admissible":
        errors.append("allow_without_admissibility")
    return errors


def main() -> None:
    request = load(REQUEST_PATH)
    result = load(RESULT_PATH)

    assert correlate(request, result) == []
    assert len(result["result_receipt_hash"]) == 64
    int(result["result_receipt_hash"], 16)

    mismatched = deepcopy(result)
    mismatched["request_id"] = "rtgtt-other"
    assert "request_id_mismatch" in correlate(request, mismatched)

    unknown_evidence = deepcopy(result)
    unknown_evidence["evidence_refs_evaluated"].append("evidence://unknown/item")
    assert "unknown_evidence_ref" in correlate(request, unknown_evidence)

    invalid_execution = deepcopy(result)
    invalid_execution["commit_authorized"] = False
    invalid_execution["execution_authorized"] = True
    assert "execution_without_commit" in correlate(request, invalid_execution)

    denied_but_authorized = deepcopy(result)
    denied_but_authorized["resolution"] = "DENY"
    denied_but_authorized["admissibility"] = "inadmissible"
    denied_but_authorized["commit_authorized"] = True
    assert "deny_with_authorization" in correlate(request, denied_but_authorized)

    receipt_payload = {key: value for key, value in result.items() if key != "result_receipt_hash"}
    assert len(canonical_hash(receipt_payload)) == 64

    print("RTG-TT result contract tests passed.")


if __name__ == "__main__":
    main()
