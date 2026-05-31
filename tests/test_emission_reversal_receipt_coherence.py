#!/usr/bin/env python3
"""Provisional RTG emission reversal receipt coherence tests."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "emission-reversal-receipt-coherence.valid.json"

VALID_STATES = {
    "coherent",
    "authority_failure",
    "replay_failure",
    "lineage_or_receipt_failure",
    "quarantine_required",
    "provisional_review",
}

def classify(case: dict[str, Any]) -> str:
    if case["risk"] > 0.60:
        return "quarantine_required"
    if not case["authority"]:
        return "authority_failure"
    if not case["replay"]:
        return "replay_failure"
    if not case["lineage_or_receipt"]:
        return "lineage_or_receipt_failure"
    if case["confidence"] < 0.65:
        return "provisional_review"
    return "coherent"

def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError("fixture must be a JSON object.")
    return payload

def validate(payload: dict[str, Any]) -> None:
    if payload.get("layer_type") != "cross-layer coherence":
        raise AssertionError("layer_type must be cross-layer coherence.")
    if set(payload.get("valid_states", [])) != VALID_STATES:
        raise AssertionError("valid_states mismatch.")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise AssertionError("cases must be a non-empty list.")
    seen = set()
    for case in cases:
        if case["case_id"] in seen:
            raise AssertionError(f"duplicate case_id: {case['case_id']}")
        seen.add(case["case_id"])
        for field in ["authority", "replay", "lineage_or_receipt"]:
            if not isinstance(case[field], bool):
                raise AssertionError(f"{case['case_id']}.{field} must be boolean.")
        for field in ["risk", "confidence"]:
            if not isinstance(case[field], (int, float)) or not 0 <= case[field] <= 1:
                raise AssertionError(f"{case['case_id']}.{field} must be within 0..1.")
        if case["expected_state"] not in VALID_STATES:
            raise AssertionError(f"{case['case_id']} expected_state invalid.")

def test_all_states_covered(payload: dict[str, Any]) -> None:
    seen = {case["expected_state"] for case in payload["cases"]}
    missing = sorted(VALID_STATES - seen)
    if missing:
        raise AssertionError(f"Fixture missing states: {missing}")

def test_classification(payload: dict[str, Any]) -> None:
    for case in payload["cases"]:
        actual = classify(case)
        expected = case["expected_state"]
        if actual != expected:
            raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}.")

def main() -> None:
    payload = load_fixture()
    validate(payload)
    test_all_states_covered(payload)
    test_classification(payload)
    print("RTG emission reversal receipt coherence tests passed.")

if __name__ == "__main__":
    main()
