#!/usr/bin/env python3
"""Provisional RTG function-class behavior tests.

These tests do not prove Relative Transition Geometry.
They validate that function-class labels now carry minimal executable behavior.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "function-classes.valid.json"

EXPECTED_CLASSES = {
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

REQUIRED_PROFILE_FIELDS = {
    "class_name",
    "description",
    "pressure_growth",
    "observation_effect",
    "coupling_effect",
    "stabilization_difficulty",
    "emission_constraint",
    "zeno_sensitivity",
    "expected_behavior",
}

UNIT_INTERVAL_FIELDS = {
    "pressure_growth",
    "observation_effect",
    "stabilization_difficulty",
    "emission_constraint",
    "zeno_sensitivity",
}


def load_profiles() -> dict[str, dict[str, Any]]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    profiles = payload.get("profiles")
    if not isinstance(profiles, list):
        raise AssertionError("profiles must be a list.")

    by_name: dict[str, dict[str, Any]] = {}

    for index, profile in enumerate(profiles):
        if not isinstance(profile, dict):
            raise AssertionError(f"profile at index {index} must be an object.")

        missing = sorted(REQUIRED_PROFILE_FIELDS - set(profile))
        if missing:
            raise AssertionError(f"profile at index {index} missing fields: {missing}")

        class_name = profile["class_name"]
        if not isinstance(class_name, str):
            raise AssertionError(f"profile at index {index} has invalid class_name.")

        if class_name in by_name:
            raise AssertionError(f"duplicate function class: {class_name}")

        by_name[class_name] = profile

    missing_classes = sorted(EXPECTED_CLASSES - set(by_name))
    if missing_classes:
        raise AssertionError(f"missing function classes: {missing_classes}")

    unexpected_classes = sorted(set(by_name) - EXPECTED_CLASSES)
    if unexpected_classes:
        raise AssertionError(f"unexpected function classes: {unexpected_classes}")

    return by_name


def assert_unit_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")

    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def assert_signed_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")

    if not -1 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between -1 and 1.")


def main() -> None:
    profiles = load_profiles()

    for class_name, profile in profiles.items():
        for field in UNIT_INTERVAL_FIELDS:
            assert_unit_interval(f"{class_name}.{field}", profile[field])
        assert_signed_interval(f"{class_name}.coupling_effect", profile["coupling_effect"])

    bounded = profiles["bounded"]
    slow = profiles["slow_growth"]
    steep = profiles["steep_growth"]
    singular = profiles["singular"]
    dampening = profiles["dampening"]
    amplifying = profiles["amplifying"]
    bridging = profiles["bridging"]
    barrier = profiles["barrier"]
    resonant = profiles["resonant"]

    if not bounded["pressure_growth"] < slow["pressure_growth"] < steep["pressure_growth"] < singular["pressure_growth"]:
        raise AssertionError("Expected bounded < slow_growth < steep_growth < singular pressure growth.")

    if singular["pressure_growth"] != max(profile["pressure_growth"] for profile in profiles.values()):
        raise AssertionError("singular must have the highest pressure_growth.")

    if singular["zeno_sensitivity"] < 0.80:
        raise AssertionError("singular must have high zeno_sensitivity.")

    if bounded["pressure_growth"] > 0.50 or bounded["zeno_sensitivity"] > 0.50:
        raise AssertionError("bounded must stay below runaway thresholds.")

    if dampening["coupling_effect"] >= 0:
        raise AssertionError("dampening must reduce propagation with negative coupling_effect.")

    if amplifying["coupling_effect"] <= 0:
        raise AssertionError("amplifying must increase propagation with positive coupling_effect.")

    if bridging["coupling_effect"] <= 0:
        raise AssertionError("bridging must have positive coupling_effect.")

    if barrier["coupling_effect"] > 0:
        raise AssertionError("barrier must not have positive coupling_effect.")

    if barrier["emission_constraint"] < 0.80:
        raise AssertionError("barrier must strongly constrain emission.")

    if bridging["emission_constraint"] >= barrier["emission_constraint"]:
        raise AssertionError("bridging emission_constraint must be lower than barrier.")

    if resonant["coupling_effect"] <= 0 or resonant["zeno_sensitivity"] < 0.50:
        raise AssertionError("resonant must support positive coupling and moderate-to-high Zeno sensitivity.")

    print("RTG function-class behavior tests passed.")


if __name__ == "__main__":
    main()
