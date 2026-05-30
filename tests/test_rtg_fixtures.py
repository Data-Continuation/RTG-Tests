#!/usr/bin/env python3
"""Minimal RTG fixture smoke tests.

These tests validate fixture shape only.
They do not prove Relative Transition Geometry.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VALID_MATURITY = {
    "draft",
    "speculative",
    "provisional",
    "tested",
    "proven",
    "deprecated",
}

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

VALID_SHELL_ROLES = {"s", "p", "d", "f"}

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

VALID_RELATION_TYPES = {
    "shared_evidence",
    "shared_authority",
    "shared_policy",
    "shared_risk",
    "shared_observer_limit",
    "shared_replay_path",
    "dependency",
    "analogy",
    "resonance",
    "barrier",
}

BOUNDED_CELL_FIELDS = {
    "observation",
    "evidence_density",
    "confidence",
    "admissibility_pressure",
    "risk_resistance",
    "stabilization",
    "emission_readiness",
    "darkness",
}

COUPLING_EFFECT_FIELDS = {
    "translation_weight",
    "pressure_effect",
    "confidence_effect",
    "darkness_effect",
    "emission_effect",
}


def load_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def assert_number(name: str, value: object) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")


def assert_unit_interval(name: str, value: object) -> None:
    assert_number(name, value)
    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def test_cell_state_fixture() -> None:
    cell = load_json("fixtures/cell-state.example.json")

    required_fields = {
        "cell_id",
        "label",
        "maturity",
        "function_class",
        "shell_role",
        "governance_posture",
        "notes",
        *BOUNDED_CELL_FIELDS,
    }

    missing = sorted(required_fields - set(cell))
    if missing:
        raise AssertionError(f"Cell fixture missing fields: {missing}")

    if cell["maturity"] not in VALID_MATURITY:
        raise AssertionError("Invalid maturity value.")

    if cell["function_class"] not in VALID_FUNCTION_CLASSES:
        raise AssertionError("Invalid function_class value.")

    if cell["shell_role"] not in VALID_SHELL_ROLES:
        raise AssertionError("Invalid shell_role value.")

    if cell["governance_posture"] not in VALID_GOVERNANCE_POSTURES:
        raise AssertionError("Invalid governance_posture value.")

    for field in BOUNDED_CELL_FIELDS:
        assert_unit_interval(field, cell[field])


def test_coupling_fixture() -> None:
    payload = load_json("fixtures/coupling.example.json")

    if "couplings" not in payload:
        raise AssertionError("Coupling fixture must contain couplings.")

    if not isinstance(payload["couplings"], list) or not payload["couplings"]:
        raise AssertionError("couplings must be a non-empty list.")

    required_fields = {
        "source_cell",
        "target_cell",
        "relation_type",
        "translation_weight",
        "pressure_effect",
        "confidence_effect",
        "darkness_effect",
        "emission_effect",
        "notes",
    }

    for index, coupling in enumerate(payload["couplings"]):
        missing = sorted(required_fields - set(coupling))
        if missing:
            raise AssertionError(f"Coupling {index} missing fields: {missing}")

        if coupling["relation_type"] not in VALID_RELATION_TYPES:
            raise AssertionError(f"Coupling {index} has invalid relation_type.")

        assert_unit_interval("translation_weight", coupling["translation_weight"])

        for field in COUPLING_EFFECT_FIELDS - {"translation_weight"}:
            assert_number(field, coupling[field])
            if not -1 <= float(coupling[field]) <= 1:
                raise AssertionError(f"{field} must be between -1 and 1.")


def main() -> None:
    test_cell_state_fixture()
    test_coupling_fixture()
    print("RTG fixture smoke tests passed.")


if __name__ == "__main__":
    main()
