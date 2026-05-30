#!/usr/bin/env python3
"""Provisional RTG Zeno-prone transition tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "zeno-transitions.valid.json"

VALID_FUNCTION_CLASSES = {
    "bounded",
    "slow_growth",
    "steep_growth",
    "singular",
    "dampening",
    "amplifying",
    "bridging",
    "barrier",
    "resonant",
}

VALID_TRANSITION_STATES = {"supported", "slowed", "frozen"}

NUMERIC_FIELDS = {
    "observation_frequency",
    "zeno_sensitivity",
    "stabilization_before",
    "stabilization_after",
    "emission_before",
    "emission_after",
}

REQUIRED_CASE_FIELDS = {
    "case_id",
    "function_class",
    "expected_transition_state",
    *NUMERIC_FIELDS,
}

SLOWED_EMISSION_TOLERANCE = 0.05


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise AssertionError("Zeno transition fixture must be a JSON object.")

    return payload


def assert_unit_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")

    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def zeno_pressure(case: dict[str, Any]) -> float:
    return float(case["observation_frequency"]) * float(case["zeno_sensitivity"])


def classify_by_pressure(case: dict[str, Any], thresholds: dict[str, Any]) -> str:
    pressure = zeno_pressure(case)

    if pressure < float(thresholds["supported_max_exclusive"]):
        return "supported"

    if float(thresholds["slowed_min_inclusive"]) <= pressure <= float(thresholds["slowed_max_inclusive"]):
        return "slowed"

    if pressure > float(thresholds["frozen_min_exclusive"]):
        return "frozen"

    raise AssertionError(f"Zeno pressure {pressure} did not map to a transition class.")


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

        if case["function_class"] not in VALID_FUNCTION_CLASSES:
            raise AssertionError(f"{case_id} has invalid function_class.")

        if case["expected_transition_state"] not in VALID_TRANSITION_STATES:
            raise AssertionError(f"{case_id} has invalid expected_transition_state.")

        for field in NUMERIC_FIELDS:
            assert_unit_interval(f"{case_id}.{field}", case[field])


def test_fixture_covers_all_transition_states(cases: list[dict[str, Any]]) -> None:
    states = {case["expected_transition_state"] for case in cases}
    missing = sorted(VALID_TRANSITION_STATES - states)

    if missing:
        raise AssertionError(f"Fixture missing transition states: {missing}")


def test_pressure_classification(cases: list[dict[str, Any]], thresholds: dict[str, Any]) -> None:
    for case in cases:
        actual = classify_by_pressure(case, thresholds)
        expected = case["expected_transition_state"]

        if actual != expected:
            raise AssertionError(f"{case['case_id']} expected {expected} by pressure, got {actual}.")


def test_transition_dynamics(cases: list[dict[str, Any]]) -> None:
    for case in cases:
        state = case["expected_transition_state"]
        stabilization_before = float(case["stabilization_before"])
        stabilization_after = float(case["stabilization_after"])
        emission_before = float(case["emission_before"])
        emission_after = float(case["emission_after"])

        if state == "supported":
            if stabilization_after <= stabilization_before:
                raise AssertionError(f"{case['case_id']} supported transition must improve stabilization.")
            if emission_after < emission_before:
                raise AssertionError(f"{case['case_id']} supported transition must not reduce emission.")

        if state == "slowed":
            if stabilization_after < stabilization_before:
                raise AssertionError(f"{case['case_id']} slowed transition must not regress stabilization.")
            if emission_after > emission_before + SLOWED_EMISSION_TOLERANCE:
                raise AssertionError(f"{case['case_id']} slowed transition must not advance emission too strongly.")

        if state == "frozen":
            if stabilization_after > stabilization_before:
                raise AssertionError(f"{case['case_id']} frozen transition must not improve stabilization.")
            if emission_after > emission_before:
                raise AssertionError(f"{case['case_id']} frozen transition must not improve emission.")


def main() -> None:
    payload = load_fixture()
    cases = payload.get("cases")
    thresholds = payload.get("thresholds")

    if not isinstance(cases, list):
        raise AssertionError("Fixture must contain cases list.")

    if not isinstance(thresholds, dict):
        raise AssertionError("Fixture must contain thresholds object.")

    validate_cases(cases)
    test_fixture_covers_all_transition_states(cases)
    test_pressure_classification(cases, thresholds)
    test_transition_dynamics(cases)

    print("RTG Zeno transition tests passed.")


if __name__ == "__main__":
    main()
