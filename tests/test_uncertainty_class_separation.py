#!/usr/bin/env python3
"""Provisional RTG uncertainty-class separation tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "uncertainty-classes.valid.json"

VALID_UNCERTAINTY_CLASSES = {"false_transition", "unknown_unknown"}
NUMERIC_FIELDS = {"claim_integrity", "model_visibility"}
REQUIRED_CASE_FIELDS = {
    "case_id", "apparent_transition", "valid_transition", "claim_integrity",
    "model_visibility", "known_invalid_signal", "unmodeled_external_factor",
    "subtype", "expected_uncertainty_class", "expected_governance_output",
}


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError("Uncertainty-class fixture must be a JSON object.")
    return payload


def assert_unit_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")
    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def classify_uncertainty(case: dict[str, Any]) -> str:
    if bool(case["known_invalid_signal"]):
        return "false_transition"
    if case["apparent_transition"] is True and case["valid_transition"] is False:
        return "false_transition"
    if bool(case["unmodeled_external_factor"]):
        return "unknown_unknown"
    if case["valid_transition"] is None:
        return "unknown_unknown"
    raise AssertionError(f"{case['case_id']} cannot be classified by provisional rules.")


def validate_fixture(payload: dict[str, Any]) -> None:
    if set(payload.get("classes", [])) != VALID_UNCERTAINTY_CLASSES:
        raise AssertionError("classes must exactly separate false_transition and unknown_unknown.")
    if not payload.get("valid_false_transition_subtypes"):
        raise AssertionError("valid_false_transition_subtypes must be non-empty.")
    if not payload.get("valid_unknown_unknown_subtypes"):
        raise AssertionError("valid_unknown_unknown_subtypes must be non-empty.")
    outputs = payload.get("allowed_governance_outputs")
    if not isinstance(outputs, dict) or set(outputs) != VALID_UNCERTAINTY_CLASSES:
        raise AssertionError("allowed_governance_outputs must define both uncertainty classes.")
    if not isinstance(payload.get("cases"), list) or not payload["cases"]:
        raise AssertionError("cases must be a non-empty list.")


def validate_cases(payload: dict[str, Any]) -> None:
    false_subtypes = set(payload["valid_false_transition_subtypes"])
    unknown_subtypes = set(payload["valid_unknown_unknown_subtypes"])
    governance_outputs = payload["allowed_governance_outputs"]
    seen_ids: set[str] = set()

    for index, case in enumerate(payload["cases"]):
        missing = sorted(REQUIRED_CASE_FIELDS - set(case))
        if missing:
            raise AssertionError(f"case at index {index} missing fields: {missing}")
        case_id = case["case_id"]
        if not isinstance(case_id, str) or not case_id:
            raise AssertionError(f"case at index {index} has invalid case_id.")
        if case_id in seen_ids:
            raise AssertionError(f"duplicate case_id: {case_id}")
        seen_ids.add(case_id)

        for boolean_field in ["apparent_transition", "known_invalid_signal", "unmodeled_external_factor"]:
            if not isinstance(case[boolean_field], bool):
                raise AssertionError(f"{case_id}.{boolean_field} must be boolean.")
        if case["valid_transition"] not in {True, False, None}:
            raise AssertionError(f"{case_id}.valid_transition must be true, false, or null.")
        for field in NUMERIC_FIELDS:
            assert_unit_interval(f"{case_id}.{field}", case[field])

        cls = case["expected_uncertainty_class"]
        if cls not in VALID_UNCERTAINTY_CLASSES:
            raise AssertionError(f"{case_id} has invalid expected_uncertainty_class.")
        if cls == "false_transition" and case["subtype"] not in false_subtypes:
            raise AssertionError(f"{case_id} has invalid false-transition subtype.")
        if cls == "unknown_unknown" and case["subtype"] not in unknown_subtypes:
            raise AssertionError(f"{case_id} has invalid unknown-unknown subtype.")
        if case["expected_governance_output"] not in set(governance_outputs[cls]):
            raise AssertionError(f"{case_id} governance output is invalid for {cls}.")


def test_classification(payload: dict[str, Any]) -> None:
    for case in payload["cases"]:
        actual = classify_uncertainty(case)
        expected = case["expected_uncertainty_class"]
        if actual != expected:
            raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}.")


def test_fixture_covers_both_uncertainty_classes(payload: dict[str, Any]) -> None:
    seen = {case["expected_uncertainty_class"] for case in payload["cases"]}
    missing = sorted(VALID_UNCERTAINTY_CLASSES - seen)
    if missing:
        raise AssertionError(f"Fixture missing uncertainty classes: {missing}")


def test_governance_outputs_do_not_cross(payload: dict[str, Any]) -> None:
    unknown_outputs = set(payload["allowed_governance_outputs"]["unknown_unknown"])
    false_outputs = set(payload["allowed_governance_outputs"]["false_transition"])
    for case in payload["cases"]:
        cls = case["expected_uncertainty_class"]
        output = case["expected_governance_output"]
        if cls == "false_transition" and output in unknown_outputs:
            raise AssertionError(f"{case['case_id']} false transition used unknown-unknown governance.")
        if cls == "unknown_unknown" and output in false_outputs:
            raise AssertionError(f"{case['case_id']} unknown unknown used false-transition governance.")


def test_class_specific_requirements(payload: dict[str, Any]) -> None:
    for case in payload["cases"]:
        cls = case["expected_uncertainty_class"]
        if cls == "false_transition":
            if not case["known_invalid_signal"] and case["valid_transition"] is not False:
                raise AssertionError(f"{case['case_id']} false transition lacks invalidity.")
        if cls == "unknown_unknown":
            if case["known_invalid_signal"]:
                raise AssertionError(f"{case['case_id']} unknown unknown cannot have known invalid signal.")
            if not case["unmodeled_external_factor"] and case["valid_transition"] is not None:
                raise AssertionError(f"{case['case_id']} unknown unknown must preserve model limitation.")


def main() -> None:
    payload = load_fixture()
    validate_fixture(payload)
    validate_cases(payload)
    test_fixture_covers_both_uncertainty_classes(payload)
    test_classification(payload)
    test_governance_outputs_do_not_cross(payload)
    test_class_specific_requirements(payload)
    print("RTG uncertainty-class separation tests passed.")


if __name__ == "__main__":
    main()
