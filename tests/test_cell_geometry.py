#!/usr/bin/env python3
"""First provisional RTG cell-geometry smoke tests.

These tests do not prove Relative Transition Geometry.
They only validate basic coherence of early cell-geometry fixtures.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "cell-geometry.valid.json"

VALID_MATURITY = {
    "draft",
    "speculative",
    "provisional",
    "tested",
    "proven",
    "deprecated",
}

VALID_SHELL_ROLES = {"s", "p", "d", "f"}

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

VALID_GOVERNANCE_POSTURES = {
    "accepted",
    "rejected",
    "deferred",
    "quarantined",
    "superseded",
    "unresolved",
    "contested",
    "unknown",
}

UNIT_INTERVAL_FIELDS = {
    "observation",
    "darkness",
    "evidence_density",
    "confidence",
    "admissibility_pressure",
    "risk_resistance",
    "stabilization",
    "emission_readiness",
}

REQUIRED_FIELDS = {
    "cell_id",
    "maturity",
    "shell_role",
    "function_class",
    "governance_posture",
    *UNIT_INTERVAL_FIELDS,
}

DARKNESS_COMPLEMENT_TOLERANCE = 0.05
CONFIDENCE_SUPPORT_TOLERANCE = 0.10


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise AssertionError("Cell geometry fixture must be a JSON object.")

    return payload


def assert_unit_interval(field: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{field} must be numeric.")

    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{field} must be between 0 and 1.")


def test_required_fields(cell: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS - set(cell))
    if missing:
        raise AssertionError(f"Cell geometry fixture missing fields: {missing}")


def test_enum_fields(cell: dict[str, Any]) -> None:
    if cell["maturity"] not in VALID_MATURITY:
        raise AssertionError("Invalid maturity value.")

    if cell["shell_role"] not in VALID_SHELL_ROLES:
        raise AssertionError("Invalid shell_role value.")

    if cell["function_class"] not in VALID_FUNCTION_CLASSES:
        raise AssertionError("Invalid function_class value.")

    if cell["governance_posture"] not in VALID_GOVERNANCE_POSTURES:
        raise AssertionError("Invalid governance_posture value.")


def test_unit_interval_fields(cell: dict[str, Any]) -> None:
    for field in UNIT_INTERVAL_FIELDS:
        assert_unit_interval(field, cell[field])


def test_darkness_complements_observation(cell: dict[str, Any]) -> None:
    expected_darkness = 1 - float(cell["observation"])
    actual_darkness = float(cell["darkness"])
    delta = abs(expected_darkness - actual_darkness)

    if delta > DARKNESS_COMPLEMENT_TOLERANCE:
        raise AssertionError(
            "darkness must remain close to 1 - observation "
            f"within tolerance {DARKNESS_COMPLEMENT_TOLERANCE}."
        )


def test_emission_does_not_exceed_stabilization(cell: dict[str, Any]) -> None:
    if float(cell["emission_readiness"]) > float(cell["stabilization"]):
        raise AssertionError("emission_readiness must not exceed stabilization.")


def test_confidence_has_observation_or_evidence_support(cell: dict[str, Any]) -> None:
    support = (float(cell["observation"]) + float(cell["evidence_density"])) / 2
    ceiling = support + CONFIDENCE_SUPPORT_TOLERANCE

    if float(cell["confidence"]) > ceiling:
        raise AssertionError(
            "confidence must not outrun average observation/evidence support "
            f"plus tolerance {CONFIDENCE_SUPPORT_TOLERANCE}."
        )


def test_pressure_balance_is_numeric(cell: dict[str, Any]) -> None:
    pressure_balance = float(cell["admissibility_pressure"]) - float(cell["risk_resistance"])

    if not -1 <= pressure_balance <= 1:
        raise AssertionError("pressure_balance must remain between -1 and 1.")


def main() -> None:
    cell = load_fixture()
    test_required_fields(cell)
    test_enum_fields(cell)
    test_unit_interval_fields(cell)
    test_darkness_complements_observation(cell)
    test_emission_does_not_exceed_stabilization(cell)
    test_confidence_has_observation_or_evidence_support(cell)
    test_pressure_balance_is_numeric(cell)

    print("RTG cell geometry smoke tests passed.")


if __name__ == "__main__":
    main()
