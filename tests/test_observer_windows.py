#!/usr/bin/env python3
"""Provisional RTG observer-window tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "observer-windows.valid.json"

VALID_OBSERVATION_STATES = {
    "missed",
    "seen_unclassified",
    "classified_deferred",
    "classified_emittable",
    "overclaimed",
}

NUMERIC_FIELDS = {
    "window_scope",
    "window_duration",
    "window_resolution",
    "observer_authority",
    "evidence_access",
    "confidence",
    "target_visibility",
}

CAPACITY_FIELDS = {
    "window_scope",
    "window_duration",
    "window_resolution",
    "observer_authority",
    "evidence_access",
    "confidence",
}

REQUIRED_CASE_FIELDS = {
    "case_id",
    "claimed_emission",
    "expected_observation_state",
    *NUMERIC_FIELDS,
}

REQUIRED_THRESHOLDS = {
    "visibility_min",
    "missed_capacity_max",
    "classification_min",
    "emission_min",
    "authority_min_for_emission",
    "confidence_min_for_emission",
    "evidence_min_for_emission",
}


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise AssertionError("Observer-window fixture must be a JSON object.")

    return payload


def assert_unit_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")

    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def window_capacity(case: dict[str, Any]) -> float:
    return sum(float(case[field]) for field in CAPACITY_FIELDS) / len(CAPACITY_FIELDS)


def validate_thresholds(thresholds: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_THRESHOLDS - set(thresholds))
    if missing:
        raise AssertionError(f"Missing thresholds: {missing}")

    for field in REQUIRED_THRESHOLDS:
        assert_unit_interval(f"thresholds.{field}", thresholds[field])

    if thresholds["missed_capacity_max"] >= thresholds["classification_min"]:
        raise AssertionError("missed_capacity_max must be below classification_min.")

    if thresholds["classification_min"] >= thresholds["emission_min"]:
        raise AssertionError("classification_min must be below emission_min.")


def validate_cases(cases: list[dict[str, Any]]) -> None:
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

        if not isinstance(case["claimed_emission"], bool):
            raise AssertionError(f"{case_id}.claimed_emission must be boolean.")

        if case["expected_observation_state"] not in VALID_OBSERVATION_STATES:
            raise AssertionError(f"{case_id} has invalid expected_observation_state.")

        for field in NUMERIC_FIELDS:
            assert_unit_interval(f"{case_id}.{field}", case[field])


def is_emittable(case: dict[str, Any], thresholds: dict[str, Any]) -> bool:
    return (
        window_capacity(case) >= float(thresholds["emission_min"])
        and float(case["target_visibility"]) >= float(thresholds["visibility_min"])
        and float(case["observer_authority"]) >= float(thresholds["authority_min_for_emission"])
        and float(case["confidence"]) >= float(thresholds["confidence_min_for_emission"])
        and float(case["evidence_access"]) >= float(thresholds["evidence_min_for_emission"])
    )


def classify_observation(case: dict[str, Any], thresholds: dict[str, Any]) -> str:
    capacity = window_capacity(case)
    visibility = float(case["target_visibility"])
    claimed_emission = bool(case["claimed_emission"])

    emittable = is_emittable(case, thresholds)

    if claimed_emission and not emittable:
        return "overclaimed"

    if visibility < float(thresholds["visibility_min"]) or capacity < float(thresholds["missed_capacity_max"]):
        return "missed"

    if capacity < float(thresholds["classification_min"]):
        return "seen_unclassified"

    if capacity < float(thresholds["emission_min"]):
        return "classified_deferred"

    if emittable:
        return "classified_emittable"

    if claimed_emission:
        return "overclaimed"

    return "classified_deferred"


def test_fixture_covers_all_observation_states(cases: list[dict[str, Any]]) -> None:
    states = {case["expected_observation_state"] for case in cases}
    missing = sorted(VALID_OBSERVATION_STATES - states)

    if missing:
        raise AssertionError(f"Fixture missing observation states: {missing}")


def test_observation_classification(cases: list[dict[str, Any]], thresholds: dict[str, Any]) -> None:
    for case in cases:
        actual = classify_observation(case, thresholds)
        expected = case["expected_observation_state"]

        if actual != expected:
            raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}.")


def test_emission_requires_authority_confidence_and_evidence(
    cases: list[dict[str, Any]],
    thresholds: dict[str, Any],
) -> None:
    for case in cases:
        if case["expected_observation_state"] == "classified_emittable":
            if float(case["observer_authority"]) < float(thresholds["authority_min_for_emission"]):
                raise AssertionError(f"{case['case_id']} emitted without sufficient authority.")
            if float(case["confidence"]) < float(thresholds["confidence_min_for_emission"]):
                raise AssertionError(f"{case['case_id']} emitted without sufficient confidence.")
            if float(case["evidence_access"]) < float(thresholds["evidence_min_for_emission"]):
                raise AssertionError(f"{case['case_id']} emitted without sufficient evidence.")


def test_overclaimed_cases_are_claimed_but_not_emittable(
    cases: list[dict[str, Any]],
    thresholds: dict[str, Any],
) -> None:
    for case in cases:
        if case["expected_observation_state"] == "overclaimed":
            if not case["claimed_emission"]:
                raise AssertionError(f"{case['case_id']} overclaimed case must claim emission.")
            if is_emittable(case, thresholds):
                raise AssertionError(f"{case['case_id']} cannot be overclaimed if it is actually emittable.")


def main() -> None:
    payload = load_fixture()
    thresholds = payload.get("thresholds")
    cases = payload.get("cases")

    if not isinstance(thresholds, dict):
        raise AssertionError("Fixture must contain thresholds object.")

    if not isinstance(cases, list):
        raise AssertionError("Fixture must contain cases list.")

    validate_thresholds(thresholds)
    validate_cases(cases)
    test_fixture_covers_all_observation_states(cases)
    test_observation_classification(cases, thresholds)
    test_emission_requires_authority_confidence_and_evidence(cases, thresholds)
    test_overclaimed_cases_are_claimed_but_not_emittable(cases, thresholds)

    print("RTG observer-window tests passed.")


if __name__ == "__main__":
    main()
