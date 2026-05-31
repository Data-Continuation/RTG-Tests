#!/usr/bin/env python3
"""Provisional RTG detector quorum export coherence tests."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "detector-quorum-export-coherence.valid.json"

VALID_STATES = ['detector_quorum_export_valid', 'detector_gap', 'quorum_failure', 'export_failure', 'risk_quarantine']


def classify(case: dict[str, Any]) -> str:
    if float(case["risk"]) > 0.60:
        return "risk_quarantine"
    if not case["authority"]:
        return "detector_gap"
    if not case["lineage"]:
        return "quorum_failure"
    if not case["replay"]:
        return "export_failure"
    if not case["secondary_ok"]:
        return "export_failure"
    return "detector_quorum_export_valid"


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError("fixture must be a JSON object")
    return payload


def validate(payload: dict[str, Any]) -> None:
    if payload.get("layer_type") != "cross-layer coherence next-31":
        raise AssertionError("layer_type must be cross-layer coherence next-31")
    states = payload.get("valid_states")
    if states != VALID_STATES:
        raise AssertionError("valid_states do not match expected states")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise AssertionError("cases must be a non-empty list")
    seen = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise AssertionError(f"case {index} must be an object")
        for field in ["case_id", "authority", "lineage", "replay", "risk", "secondary_ok", "expected_state"]:
            if field not in case:
                raise AssertionError(f"case {index} missing {field}")
        if case["case_id"] in seen:
            raise AssertionError(f"duplicate case_id: {case['case_id']}")
        seen.add(case["case_id"])
        for field in ["authority", "lineage", "replay", "secondary_ok"]:
            if not isinstance(case[field], bool):
                raise AssertionError(f"{case['case_id']}.{field} must be boolean")
        if not isinstance(case["risk"], (int, float)) or not 0 <= float(case["risk"]) <= 1:
            raise AssertionError(f"{case['case_id']}.risk must be numeric within 0..1")
        if case["expected_state"] not in VALID_STATES:
            raise AssertionError(f"{case['case_id']} expected_state is invalid")


def test_all_states_covered(payload: dict[str, Any]) -> None:
    seen = {case["expected_state"] for case in payload["cases"]}
    missing = sorted(set(VALID_STATES) - seen)
    if missing:
        raise AssertionError(f"Fixture missing states: {missing}")


def test_classification(payload: dict[str, Any]) -> None:
    for case in payload["cases"]:
        actual = classify(case)
        expected = case["expected_state"]
        if actual != expected:
            raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}")


def main() -> None:
    payload = load_fixture()
    validate(payload)
    test_all_states_covered(payload)
    test_classification(payload)
    print("RTG detector quorum export coherence tests passed.")


if __name__ == "__main__":
    main()
