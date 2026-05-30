#!/usr/bin/env python3
"""Provisional RTG coupling translation tests.

These tests do not prove Relative Transition Geometry.
They validate a first executable rule for translated cell-to-cell influence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "coupling-translation.valid.json"

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

POSTURE_FIELDS = {
    "admissibility_pressure",
    "confidence",
    "darkness",
    "emission_readiness",
}

EFFECT_FIELDS = {
    "pressure_effect": "admissibility_pressure",
    "confidence_effect": "confidence",
    "darkness_effect": "darkness",
    "emission_effect": "emission_readiness",
}

EPSILON = 1e-9


def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise AssertionError("Coupling translation fixture must be a JSON object.")

    return payload


def assert_number(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")


def assert_unit_interval(name: str, value: Any) -> None:
    assert_number(name, value)
    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def assert_signed_interval(name: str, value: Any) -> None:
    assert_number(name, value)
    if not -1 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between -1 and 1.")


def clamp_unit(value: float) -> float:
    return max(0.0, min(1.0, value))


def indexed_by_cell_id(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}

    for index, item in enumerate(items):
        cell_id = item.get("cell_id")
        if not isinstance(cell_id, str) or not cell_id:
            raise AssertionError(f"{label} at index {index} has invalid cell_id.")

        if cell_id in by_id:
            raise AssertionError(f"Duplicate {label} cell_id: {cell_id}")

        by_id[cell_id] = item

    return by_id


def validate_fixture_shape(payload: dict[str, Any]) -> None:
    for key in ["source_cells", "target_cells", "couplings", "expected_targets_after_translation"]:
        if key not in payload:
            raise AssertionError(f"Missing fixture key: {key}")
        if not isinstance(payload[key], list) or not payload[key]:
            raise AssertionError(f"{key} must be a non-empty list.")


def validate_targets(targets: dict[str, dict[str, Any]]) -> None:
    for cell_id, target in targets.items():
        missing = sorted(POSTURE_FIELDS - set(target))
        if missing:
            raise AssertionError(f"Target {cell_id} missing fields: {missing}")

        for field in POSTURE_FIELDS:
            assert_unit_interval(f"{cell_id}.{field}", target[field])


def validate_couplings(
    couplings: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    targets: dict[str, dict[str, Any]],
) -> None:
    required = {
        "source_cell",
        "target_cell",
        "relation_type",
        "translation_weight",
        *EFFECT_FIELDS.keys(),
    }

    for index, coupling in enumerate(couplings):
        missing = sorted(required - set(coupling))
        if missing:
            raise AssertionError(f"Coupling {index} missing fields: {missing}")

        source_cell = coupling["source_cell"]
        target_cell = coupling["target_cell"]

        if source_cell not in sources:
            raise AssertionError(f"Coupling {index} references unknown source cell: {source_cell}")

        if target_cell not in targets:
            raise AssertionError(f"Coupling {index} references unknown target cell: {target_cell}")

        if coupling["relation_type"] not in VALID_RELATION_TYPES:
            raise AssertionError(f"Coupling {index} has invalid relation_type.")

        assert_unit_interval(f"coupling[{index}].translation_weight", coupling["translation_weight"])

        for effect_field in EFFECT_FIELDS:
            assert_signed_interval(f"coupling[{index}].{effect_field}", coupling[effect_field])


def apply_couplings(
    targets: dict[str, dict[str, Any]],
    couplings: list[dict[str, Any]],
) -> dict[str, dict[str, float]]:
    updated = {
        cell_id: {field: float(target[field]) for field in POSTURE_FIELDS}
        for cell_id, target in targets.items()
    }

    for coupling in couplings:
        target_cell = coupling["target_cell"]
        weight = float(coupling["translation_weight"])

        for effect_field, target_field in EFFECT_FIELDS.items():
            translated_effect = float(coupling[effect_field]) * weight
            updated[target_cell][target_field] = clamp_unit(
                updated[target_cell][target_field] + translated_effect
            )

    return updated


def assert_expected_targets(
    updated: dict[str, dict[str, float]],
    expected_items: list[dict[str, Any]],
) -> None:
    expected = indexed_by_cell_id(expected_items, "expected target")

    if set(updated) != set(expected):
        raise AssertionError("Updated target set does not match expected target set.")

    for cell_id, expected_target in expected.items():
        for field in POSTURE_FIELDS:
            assert_unit_interval(f"expected.{cell_id}.{field}", expected_target[field])
            actual = updated[cell_id][field]
            expected_value = float(expected_target[field])

            if abs(actual - expected_value) > EPSILON:
                raise AssertionError(
                    f"{cell_id}.{field} expected {expected_value}, got {actual}"
                )


def test_shared_evidence_behavior(couplings: list[dict[str, Any]]) -> None:
    shared = [item for item in couplings if item["relation_type"] == "shared_evidence"]
    if not shared:
        raise AssertionError("Fixture must include a shared_evidence coupling.")

    for coupling in shared:
        if coupling["confidence_effect"] <= 0:
            raise AssertionError("shared_evidence should raise confidence in this layer.")
        if coupling["darkness_effect"] >= 0:
            raise AssertionError("shared_evidence should reduce darkness in this layer.")


def test_barrier_behavior(couplings: list[dict[str, Any]]) -> None:
    barriers = [item for item in couplings if item["relation_type"] == "barrier"]
    if not barriers:
        raise AssertionError("Fixture must include a barrier coupling.")

    for coupling in barriers:
        if coupling["pressure_effect"] <= 0:
            raise AssertionError("barrier should raise admissibility pressure in this layer.")
        if coupling["emission_effect"] >= 0:
            raise AssertionError("barrier should lower emission readiness in this layer.")


def main() -> None:
    payload = load_fixture()
    validate_fixture_shape(payload)

    sources = indexed_by_cell_id(payload["source_cells"], "source")
    targets = indexed_by_cell_id(payload["target_cells"], "target")

    validate_targets(targets)
    validate_couplings(payload["couplings"], sources, targets)

    updated = apply_couplings(targets, payload["couplings"])
    assert_expected_targets(updated, payload["expected_targets_after_translation"])

    test_shared_evidence_behavior(payload["couplings"])
    test_barrier_behavior(payload["couplings"])

    print("RTG coupling translation tests passed.")


if __name__ == "__main__":
    main()
