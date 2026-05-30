#!/usr/bin/env python3
"""Provisional RTG shell-role expectation tests.

These tests do not prove Relative Transition Geometry.
They validate that s/p/d/f shell roles carry minimal executable expectations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "shell-roles.valid.json"

EXPECTED_ROLES = {"s", "p", "d", "f"}

REQUIRED_PROFILE_FIELDS = {
    "role",
    "description",
    "stabilization_bias",
    "coupling_reach",
    "authority_complexity",
    "latent_complexity",
    "observability_burden",
    "emission_latency",
    "ambiguity_tolerance",
    "expected_behavior",
}

NUMERIC_FIELDS = {
    "stabilization_bias",
    "coupling_reach",
    "authority_complexity",
    "latent_complexity",
    "observability_burden",
    "emission_latency",
    "ambiguity_tolerance",
}


def load_roles() -> dict[str, dict[str, Any]]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    roles = payload.get("roles")
    if not isinstance(roles, list):
        raise AssertionError("roles must be a list.")

    by_role: dict[str, dict[str, Any]] = {}

    for index, role_profile in enumerate(roles):
        if not isinstance(role_profile, dict):
            raise AssertionError(f"role profile at index {index} must be an object.")

        missing = sorted(REQUIRED_PROFILE_FIELDS - set(role_profile))
        if missing:
            raise AssertionError(f"role profile at index {index} missing fields: {missing}")

        role = role_profile["role"]
        if role not in EXPECTED_ROLES:
            raise AssertionError(f"unexpected role: {role}")

        if role in by_role:
            raise AssertionError(f"duplicate role: {role}")

        by_role[role] = role_profile

    missing_roles = sorted(EXPECTED_ROLES - set(by_role))
    if missing_roles:
        raise AssertionError(f"missing shell roles: {missing_roles}")

    return by_role


def assert_unit_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)):
        raise AssertionError(f"{name} must be numeric.")

    if not 0 <= float(value) <= 1:
        raise AssertionError(f"{name} must be between 0 and 1.")


def test_numeric_ranges(roles: dict[str, dict[str, Any]]) -> None:
    for role, profile in roles.items():
        for field in NUMERIC_FIELDS:
            assert_unit_interval(f"{role}.{field}", profile[field])


def test_latent_complexity_order(roles: dict[str, dict[str, Any]]) -> None:
    if not (
        roles["s"]["latent_complexity"]
        < roles["p"]["latent_complexity"]
        < roles["d"]["latent_complexity"]
        < roles["f"]["latent_complexity"]
    ):
        raise AssertionError("Expected s < p < d < f latent complexity.")


def test_coupling_reach_expectations(roles: dict[str, dict[str, Any]]) -> None:
    if not roles["s"]["coupling_reach"] < roles["p"]["coupling_reach"]:
        raise AssertionError("p must have greater coupling reach than s.")

    if not roles["p"]["coupling_reach"] <= roles["d"]["coupling_reach"]:
        raise AssertionError("d must have at least p-level coupling reach.")

    if not roles["d"]["coupling_reach"] <= roles["f"]["coupling_reach"]:
        raise AssertionError("f must have at least d-level coupling reach.")


def test_f_role_has_highest_observability_burden_and_latency(
    roles: dict[str, dict[str, Any]]
) -> None:
    max_burden = max(profile["observability_burden"] for profile in roles.values())
    max_latency = max(profile["emission_latency"] for profile in roles.values())

    if roles["f"]["observability_burden"] != max_burden:
        raise AssertionError("f must have the highest observability burden.")

    if roles["f"]["emission_latency"] != max_latency:
        raise AssertionError("f must have the highest emission latency.")


def test_s_role_is_foundational_stabilizer(roles: dict[str, dict[str, Any]]) -> None:
    s_role = roles["s"]

    if s_role["stabilization_bias"] < 0.80:
        raise AssertionError("s role must have high stabilization bias.")

    if s_role["ambiguity_tolerance"] > 0.35:
        raise AssertionError("s role must have low ambiguity tolerance.")

    if s_role["coupling_reach"] > 0.35:
        raise AssertionError("s role must have low coupling reach.")


def test_d_role_has_higher_authority_complexity_than_p(
    roles: dict[str, dict[str, Any]]
) -> None:
    if roles["d"]["authority_complexity"] <= roles["p"]["authority_complexity"]:
        raise AssertionError("d role must have higher authority complexity than p.")


def main() -> None:
    roles = load_roles()
    test_numeric_ranges(roles)
    test_latent_complexity_order(roles)
    test_coupling_reach_expectations(roles)
    test_f_role_has_highest_observability_burden_and_latency(roles)
    test_s_role_is_foundational_stabilizer(roles)
    test_d_role_has_higher_authority_complexity_than_p(roles)

    print("RTG shell-role expectation tests passed.")


if __name__ == "__main__":
    main()
