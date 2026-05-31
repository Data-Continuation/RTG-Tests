#!/usr/bin/env python3
"""Provisional RTG detector uncertainty replay coherence tests."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "detector-uncertainty-replay-coherence.valid.json"

def classify(c):
    if c["claimed_coverage"] and not c["detector_available"]: return "coverage_overclaim_quarantine"
    if c["uncertainty_class"] == "false_transition" and c["replay_state"] == "invalid_replay": return "false_transition_replay_rejected"
    if not c["detector_available"] and c["replay_state"] == "replay_required": return "detector_gap_replay_deferred"
    if not c["detector_available"] and c["uncertainty_class"] == "unknown_unknown": return "detector_gap_unknown_unknown"
    return "detected_replay_valid"

def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError("fixture must be a JSON object.")
    return payload

def validate(payload: dict[str, Any]) -> None:
    states = payload.get("valid_states")
    cases = payload.get("cases")
    if payload.get("layer_type") != "cross-layer coherence":
        raise AssertionError("layer_type must be cross-layer coherence.")
    if not isinstance(states, list) or not states:
        raise AssertionError("valid_states must be a non-empty list.")
    if len(states) != len(set(states)):
        raise AssertionError("valid_states must not contain duplicates.")
    if not isinstance(cases, list) or not cases:
        raise AssertionError("cases must be a non-empty list.")
    seen = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise AssertionError(f"case {index} must be an object.")
        if "case_id" not in case or "expected_state" not in case:
            raise AssertionError(f"case {index} missing case_id or expected_state.")
        if case["case_id"] in seen:
            raise AssertionError(f"duplicate case_id: {case['case_id']}")
        seen.add(case["case_id"])
        if case["expected_state"] not in states:
            raise AssertionError(f"{case['case_id']} expected_state not in valid_states.")

def test_all_states_covered(payload: dict[str, Any]) -> None:
    expected = set(payload["valid_states"])
    seen = {case["expected_state"] for case in payload["cases"]}
    missing = sorted(expected - seen)
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
    print("RTG detector uncertainty replay coherence tests passed.")

if __name__ == "__main__":
    main()
