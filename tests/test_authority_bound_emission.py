#!/usr/bin/env python3
"""Provisional RTG authority-bound emission tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "authority-bound-emission.valid.json"

VALID_AUTHORITY_EMISSION_STATES = {
    "not_visible",
    "not_ready",
    "authority_insufficient",
    "authority_satisfied",
    "overclaimed_authority",
}

NUMERIC_FIELDS = {
    "target_visibility",
    "stabilization",
    "evidence_density",
    "confidence",
    "emission_readiness",
}

REQUIRED_CASE_FIELDS = {
    "case_id",
    "transition_class",
    "observer_authority_class",
    "claimed_emission",
    "expected_authority_emission_state",
    *NUMERIC_FIELDS,
}

REQUIRED_THRESHOLDS = {
    "visibility_min",
    "stabilization_min",
    "evidence_min",
    "confidence_min",
    "emission_min",
}


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise AssertionError("Authority-bound emission fixture must be a JSON object.")

    return payload


def assert_unit_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")

    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def validate_thresholds(thresholds: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_THRESHOLDS - set(thresholds))
    if missing:
        raise AssertionError(f"Missing thresholds: {missing}")

    for field in REQUIRED_THRESHOLDS:
        assert_unit_interval(f"thresholds.{field}", thresholds[field])


def validate_authority_model(
    authority_order: list[str],
    requirements: dict[str, str],
) -> None:
    if not authority_order:
        raise AssertionError("authority_order must be non-empty.")

    if len(authority_order) != len(set(authority_order)):
        raise AssertionError("authority_order must not contain duplicates.")

    for transition_class, authority_class in requirements.items():
        if not isinstance(transition_class, str) or not transition_class:
            raise AssertionError("transition class keys must be non-empty strings.")

        if authority_class not in authority_order:
            raise AssertionError(f"{transition_class} requires unknown authority class: {authority_class}")


def authority_rank(authority_order: list[str], authority_class: str) -> int:
    if authority_class not in authority_order:
        raise AssertionError(f"Unknown authority class: {authority_class}")

    return authority_order.index(authority_class)


def authority_sufficient(
    authority_order: list[str],
    observer_authority: str,
    required_authority: str,
) -> bool:
    return authority_rank(authority_order, observer_authority) >= authority_rank(
        authority_order,
        required_authority,
    )


def is_ready(case: dict[str, Any], thresholds: dict[str, Any]) -> bool:
    return (
        float(case["stabilization"]) >= float(thresholds["stabilization_min"])
        and float(case["evidence_density"]) >= float(thresholds["evidence_min"])
        and float(case["confidence"]) >= float(thresholds["confidence_min"])
        and float(case["emission_readiness"]) >= float(thresholds["emission_min"])
    )


def classify_authority_emission(
    case: dict[str, Any],
    thresholds: dict[str, Any],
    authority_order: list[str],
    requirements: dict[str, str],
) -> str:
    transition_class = case["transition_class"]
    observer_authority = case["observer_authority_class"]

    if transition_class not in requirements:
        raise AssertionError(f"{case['case_id']} has unknown transition_class.")

    required_authority = requirements[transition_class]

    if float(case["target_visibility"]) < float(thresholds["visibility_min"]):
        return "not_visible"

    if not is_ready(case, thresholds):
        return "not_ready"

    sufficient = authority_sufficient(authority_order, observer_authority, required_authority)

    if bool(case["claimed_emission"]) and not sufficient:
        return "overclaimed_authority"

    if not sufficient:
        return "authority_insufficient"

    return "authority_satisfied"


def validate_cases(
    cases: list[dict[str, Any]],
    authority_order: list[str],
    requirements: dict[str, str],
) -> None:
    if not cases:
        raise AssertionError("cases must be non-empty.")

    seen_ids: set[str] = set()

    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise AssertionError(f"case at index {index} must be an object.")

        missing = sorted(REQUIRED_CASE_FIELDS - set(case))
        if missing:
            raise AssertionError(f"case at index {index} missing fields: {missing}")

        case_id = case["case_id"]
        if not isinstance(case_id, str) or not case_id:
            raise AssertionError(f"case at index {index} has invalid case_id.")

        if case_id in seen_ids:
            raise AssertionError(f"duplicate case_id: {case_id}")

        seen_ids.add(case_id)

        if case["transition_class"] not in requirements:
            raise AssertionError(f"{case_id} has unknown transition_class.")

        if case["observer_authority_class"] not in authority_order:
            raise AssertionError(f"{case_id} has unknown observer_authority_class.")

        if not isinstance(case["claimed_emission"], bool):
            raise AssertionError(f"{case_id}.claimed_emission must be boolean.")

        if case["expected_authority_emission_state"] not in VALID_AUTHORITY_EMISSION_STATES:
            raise AssertionError(f"{case_id} has invalid expected_authority_emission_state.")

        for field in NUMERIC_FIELDS:
            assert_unit_interval(f"{case_id}.{field}", case[field])


def test_fixture_covers_all_authority_emission_states(cases: list[dict[str, Any]]) -> None:
    states = {case["expected_authority_emission_state"] for case in cases}
    missing = sorted(VALID_AUTHORITY_EMISSION_STATES - states)

    if missing:
        raise AssertionError(f"Fixture missing authority emission states: {missing}")


def test_authority_emission_classification(
    cases: list[dict[str, Any]],
    thresholds: dict[str, Any],
    authority_order: list[str],
    requirements: dict[str, str],
) -> None:
    for case in cases:
        actual = classify_authority_emission(case, thresholds, authority_order, requirements)
        expected = case["expected_authority_emission_state"]

        if actual != expected:
            raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}.")


def test_visibility_and_readiness_do_not_substitute_for_authority(
    cases: list[dict[str, Any]],
    thresholds: dict[str, Any],
    authority_order: list[str],
    requirements: dict[str, str],
) -> None:
    for case in cases:
        visible = float(case["target_visibility"]) >= float(thresholds["visibility_min"])
        ready = is_ready(case, thresholds)
        required = requirements[case["transition_class"]]
        sufficient = authority_sufficient(authority_order, case["observer_authority_class"], required)

        if visible and ready and not sufficient:
            if case["expected_authority_emission_state"] == "authority_satisfied":
                raise AssertionError(f"{case['case_id']} incorrectly treats visibility/readiness as authority.")


def test_overclaims_require_claimed_emission(cases: list[dict[str, Any]]) -> None:
    for case in cases:
        if case["expected_authority_emission_state"] == "overclaimed_authority":
            if not case["claimed_emission"]:
                raise AssertionError(f"{case['case_id']} overclaim must claim emission.")


def main() -> None:
    payload = load_fixture()
    thresholds = payload.get("thresholds")
    authority_order = payload.get("authority_order")
    requirements = payload.get("transition_authority_requirements")
    cases = payload.get("cases")

    if not isinstance(thresholds, dict):
        raise AssertionError("Fixture must contain thresholds object.")

    if not isinstance(authority_order, list):
        raise AssertionError("Fixture must contain authority_order list.")

    if not isinstance(requirements, dict):
        raise AssertionError("Fixture must contain transition_authority_requirements object.")

    if not isinstance(cases, list):
        raise AssertionError("Fixture must contain cases list.")

    validate_thresholds(thresholds)
    validate_authority_model(authority_order, requirements)
    validate_cases(cases, authority_order, requirements)
    test_fixture_covers_all_authority_emission_states(cases)
    test_authority_emission_classification(cases, thresholds, authority_order, requirements)
    test_visibility_and_readiness_do_not_substitute_for_authority(
        cases,
        thresholds,
        authority_order,
        requirements,
    )
    test_overclaims_require_claimed_emission(cases)

    print("RTG authority-bound emission tests passed.")


if __name__ == "__main__":
    main()
