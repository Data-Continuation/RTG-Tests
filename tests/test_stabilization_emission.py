#!/usr/bin/env python3
"""Provisional RTG stabilization-emission threshold tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "stabilization-emission.valid.json"

VALID_EMISSION_STATES = {
    "ineligible",
    "deferred",
    "quarantined",
    "eligible",
    "blocked",
}

NUMERIC_FIELDS = {
    "compression_pressure",
    "stabilization",
    "evidence_density",
    "confidence",
    "admissibility_score",
    "risk_resistance",
    "emission_readiness",
}

REQUIRED_CASE_FIELDS = {
    "case_id",
    "expected_emission_state",
    *NUMERIC_FIELDS,
}

REQUIRED_THRESHOLDS = {
    "stabilization_min",
    "evidence_min",
    "confidence_min",
    "admissibility_min",
    "risk_max",
    "emission_min",
    "admissibility_block_max",
    "deferred_stabilization_min",
}


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise AssertionError("Stabilization-emission fixture must be a JSON object.")

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

    if thresholds["admissibility_block_max"] >= thresholds["admissibility_min"]:
        raise AssertionError("admissibility_block_max must be below admissibility_min.")

    if thresholds["deferred_stabilization_min"] >= thresholds["stabilization_min"]:
        raise AssertionError("deferred_stabilization_min must be below stabilization_min.")


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

        if case["expected_emission_state"] not in VALID_EMISSION_STATES:
            raise AssertionError(f"{case_id} has invalid expected_emission_state.")

        for field in NUMERIC_FIELDS:
            assert_unit_interval(f"{case_id}.{field}", case[field])


def classify_emission(case: dict[str, Any], thresholds: dict[str, Any]) -> str:
    if float(case["admissibility_score"]) < float(thresholds["admissibility_block_max"]):
        return "blocked"

    if float(case["risk_resistance"]) > float(thresholds["risk_max"]):
        return "quarantined"

    eligible = (
        float(case["stabilization"]) >= float(thresholds["stabilization_min"])
        and float(case["evidence_density"]) >= float(thresholds["evidence_min"])
        and float(case["confidence"]) >= float(thresholds["confidence_min"])
        and float(case["admissibility_score"]) >= float(thresholds["admissibility_min"])
        and float(case["risk_resistance"]) <= float(thresholds["risk_max"])
        and float(case["emission_readiness"]) >= float(thresholds["emission_min"])
    )

    if eligible:
        return "eligible"

    if (
        float(case["stabilization"]) >= float(thresholds["deferred_stabilization_min"])
        and float(case["risk_resistance"]) <= float(thresholds["risk_max"])
        and float(case["admissibility_score"]) >= float(thresholds["admissibility_block_max"])
    ):
        return "deferred"

    return "ineligible"


def test_classification(cases: list[dict[str, Any]], thresholds: dict[str, Any]) -> None:
    for case in cases:
        actual = classify_emission(case, thresholds)
        expected = case["expected_emission_state"]

        if actual != expected:
            raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}.")


def test_fixture_covers_all_emission_states(cases: list[dict[str, Any]]) -> None:
    states = {case["expected_emission_state"] for case in cases}
    missing = sorted(VALID_EMISSION_STATES - states)

    if missing:
        raise AssertionError(f"Fixture missing emission states: {missing}")


def test_compression_pressure_does_not_substitute_for_stabilization(
    cases: list[dict[str, Any]],
    thresholds: dict[str, Any],
) -> None:
    for case in cases:
        high_compression = float(case["compression_pressure"]) >= float(thresholds["stabilization_min"])
        low_stabilization = float(case["stabilization"]) < float(thresholds["deferred_stabilization_min"])

        if high_compression and low_stabilization:
            if case["expected_emission_state"] in {"eligible", "deferred"}:
                raise AssertionError(
                    f"{case['case_id']} compression pressure cannot substitute for stabilization."
                )


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
    test_fixture_covers_all_emission_states(cases)
    test_classification(cases, thresholds)
    test_compression_pressure_does_not_substitute_for_stabilization(cases, thresholds)

    print("RTG stabilization-emission tests passed.")


if __name__ == "__main__":
    main()
