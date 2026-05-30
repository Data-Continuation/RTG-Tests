#!/usr/bin/env python3
"""Provisional RTG dark-cell color emergence tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "dark-cell-color.valid.json"

POSTURE_TO_COLOR_FAMILY = {
    "accepted": "stable",
    "rejected": "prohibited",
    "deferred": "pending",
    "quarantined": "hazard",
    "superseded": "displaced",
    "unresolved": "dark",
    "contested": "contested",
    "unknown": "dark",
}

NUMERIC_FIELDS = {
    "observation",
    "evidence_density",
    "confidence",
    "stabilization",
    "emission_readiness",
    "darkness",
}

COLOR_INTENSITY_FIELDS = {
    "observation",
    "evidence_density",
    "confidence",
    "stabilization",
    "emission_readiness",
}

REQUIRED_PHASE_FIELDS = {
    "phase",
    "governance_posture",
    "expected_color_family",
    *NUMERIC_FIELDS,
}

DEFAULT_DARKNESS_TOLERANCE = 0.05
STABLE_EMISSION_THRESHOLD = 0.70


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError("Dark-cell color fixture must be a JSON object.")
    return payload


def assert_unit_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")
    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def color_intensity(phase: dict[str, Any]) -> float:
    return sum(float(phase[field]) for field in COLOR_INTENSITY_FIELDS) / len(COLOR_INTENSITY_FIELDS)


def validate_phase_shape(phases: list[dict[str, Any]]) -> None:
    if not phases:
        raise AssertionError("phases must be non-empty.")
    seen_phases: set[str] = set()
    valid_color_families = set(POSTURE_TO_COLOR_FAMILY.values())

    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            raise AssertionError(f"phase at index {index} must be an object.")
        missing = sorted(REQUIRED_PHASE_FIELDS - set(phase))
        if missing:
            raise AssertionError(f"phase at index {index} missing fields: {missing}")

        phase_name = phase["phase"]
        if not isinstance(phase_name, str) or not phase_name:
            raise AssertionError(f"phase at index {index} has invalid phase name.")
        if phase_name in seen_phases:
            raise AssertionError(f"duplicate phase name: {phase_name}")
        seen_phases.add(phase_name)

        if phase["governance_posture"] not in POSTURE_TO_COLOR_FAMILY:
            raise AssertionError(f"phase {phase_name} has invalid governance_posture.")
        if phase["expected_color_family"] not in valid_color_families:
            raise AssertionError(f"phase {phase_name} has invalid expected_color_family.")
        for field in NUMERIC_FIELDS:
            assert_unit_interval(f"{phase_name}.{field}", phase[field])


def test_dark_cell_starts_fully_dark(phases: list[dict[str, Any]]) -> None:
    first = phases[0]
    if first["expected_color_family"] != "dark":
        raise AssertionError("first phase must begin in the dark color family.")
    if float(first["darkness"]) != 1.0:
        raise AssertionError("first phase must begin fully dark.")
    if color_intensity(first) != 0.0:
        raise AssertionError("first phase must begin with zero color intensity.")


def test_darkness_complements_observation(phases: list[dict[str, Any]], tolerance: float) -> None:
    for phase in phases:
        expected_darkness = 1 - float(phase["observation"])
        if abs(expected_darkness - float(phase["darkness"])) > tolerance:
            raise AssertionError(f"{phase['phase']} darkness must be close to 1 - observation.")


def test_color_intensity_monotonic(phases: list[dict[str, Any]]) -> None:
    intensities = [color_intensity(phase) for phase in phases]
    for previous, current in zip(intensities, intensities[1:]):
        if current <= previous:
            raise AssertionError("color intensity must strictly increase across phases.")


def test_darkness_monotonic_decrease(phases: list[dict[str, Any]]) -> None:
    darkness_values = [float(phase["darkness"]) for phase in phases]
    for previous, current in zip(darkness_values, darkness_values[1:]):
        if current >= previous:
            raise AssertionError("darkness must strictly decrease across phases.")


def test_emission_is_stabilization_bound(phases: list[dict[str, Any]]) -> None:
    for phase in phases:
        if float(phase["emission_readiness"]) > float(phase["stabilization"]):
            raise AssertionError(f"{phase['phase']} emission_readiness must not exceed stabilization.")


def test_color_family_matches_governance_posture(phases: list[dict[str, Any]]) -> None:
    for phase in phases:
        expected = POSTURE_TO_COLOR_FAMILY[phase["governance_posture"]]
        if phase["expected_color_family"] != expected:
            raise AssertionError(f"{phase['phase']} expected color family {expected}.")


def test_stable_color_requires_emission_readiness(phases: list[dict[str, Any]]) -> None:
    for phase in phases:
        if phase["expected_color_family"] == "stable":
            if float(phase["emission_readiness"]) < STABLE_EMISSION_THRESHOLD:
                raise AssertionError("stable color requires sufficient emission readiness.")


def main() -> None:
    payload = load_fixture()
    phases = payload.get("phases")
    if not isinstance(phases, list):
        raise AssertionError("Fixture must contain phases list.")
    tolerance = float(payload.get("darkness_tolerance", DEFAULT_DARKNESS_TOLERANCE))

    validate_phase_shape(phases)
    test_dark_cell_starts_fully_dark(phases)
    test_darkness_complements_observation(phases, tolerance)
    test_color_intensity_monotonic(phases)
    test_darkness_monotonic_decrease(phases)
    test_emission_is_stabilization_bound(phases)
    test_color_family_matches_governance_posture(phases)
    test_stable_color_requires_emission_readiness(phases)

    print("RTG dark-cell color emergence tests passed.")


if __name__ == "__main__":
    main()
