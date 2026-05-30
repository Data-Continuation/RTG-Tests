#!/usr/bin/env python3
"""Provisional RTG observer-identity coupling tests."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "observer-identity-coupling.valid.json"
VALID_COUPLING_STATES = {"incompatible_observer","missed_window","visible_unclassified","classified_not_emittable","coupled_emittable"}
NUMERIC_FIELDS = {"window_visibility","classification_confidence","emission_authority"}
REQUIRED_CASE_FIELDS = {"case_id","observer_identity_class","transition_identity_class","window_visibility","classification_confidence","emission_authority","claimed_classification","claimed_emission","expected_coupling_state"}
REQUIRED_THRESHOLDS = {"window_visibility_min","classification_confidence_min","emission_authority_min"}
def load_fixture() -> dict[str, Any]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle: payload=json.load(handle)
    if not isinstance(payload, dict): raise AssertionError("Observer-identity coupling fixture must be a JSON object.")
    return payload
def assert_unit_interval(name: str, value: Any) -> None:
    if not isinstance(value, (int, float)): raise AssertionError(f"{name} must be numeric.")
    if not 0 <= float(value) <= 1: raise AssertionError(f"{name} must be between 0 and 1.")
def is_compatible(case: dict[str, Any], matrix: dict[str, list[str]]) -> bool:
    return case["transition_identity_class"] in matrix.get(case["observer_identity_class"], [])
def classify_coupling(case: dict[str, Any], matrix: dict[str, list[str]], thresholds: dict[str, Any]) -> str:
    if not is_compatible(case, matrix): return "incompatible_observer"
    if float(case["window_visibility"]) < float(thresholds["window_visibility_min"]): return "missed_window"
    if float(case["classification_confidence"]) < float(thresholds["classification_confidence_min"]): return "visible_unclassified"
    if float(case["emission_authority"]) < float(thresholds["emission_authority_min"]): return "classified_not_emittable"
    return "coupled_emittable"
def validate_thresholds(thresholds: dict[str, Any]) -> None:
    missing=sorted(REQUIRED_THRESHOLDS-set(thresholds))
    if missing: raise AssertionError(f"Missing thresholds: {missing}")
    for f in REQUIRED_THRESHOLDS: assert_unit_interval(f"thresholds.{f}", thresholds[f])
def validate_identity_model(payload: dict[str, Any]) -> None:
    observers=payload.get("observer_identity_classes"); transitions=payload.get("transition_identity_classes"); matrix=payload.get("compatibility_matrix")
    if not isinstance(observers,list) or not observers: raise AssertionError("observer_identity_classes must be a non-empty list.")
    if not isinstance(transitions,list) or not transitions: raise AssertionError("transition_identity_classes must be a non-empty list.")
    if not isinstance(matrix,dict): raise AssertionError("compatibility_matrix must be an object.")
    if len(set(observers)) != len(observers): raise AssertionError("observer_identity_classes must not contain duplicates.")
    if len(set(transitions)) != len(transitions): raise AssertionError("transition_identity_classes must not contain duplicates.")
    transition_set=set(transitions)
    for observer in observers:
        if observer not in matrix: raise AssertionError(f"compatibility_matrix missing observer: {observer}")
        if not isinstance(matrix[observer],list): raise AssertionError(f"compatibility_matrix.{observer} must be a list.")
        unknown=sorted(set(matrix[observer])-transition_set)
        if unknown: raise AssertionError(f"compatibility_matrix.{observer} has unknown transitions: {unknown}")
def validate_cases(payload: dict[str, Any]) -> None:
    observer_set=set(payload["observer_identity_classes"]); transition_set=set(payload["transition_identity_classes"]); seen=set()
    for index, case in enumerate(payload["cases"]):
        missing=sorted(REQUIRED_CASE_FIELDS-set(case))
        if missing: raise AssertionError(f"case at index {index} missing fields: {missing}")
        cid=case["case_id"]
        if not isinstance(cid,str) or not cid: raise AssertionError(f"case at index {index} has invalid case_id.")
        if cid in seen: raise AssertionError(f"duplicate case_id: {cid}")
        seen.add(cid)
        if case["observer_identity_class"] not in observer_set: raise AssertionError(f"{cid} has unknown observer_identity_class.")
        if case["transition_identity_class"] not in transition_set: raise AssertionError(f"{cid} has unknown transition_identity_class.")
        if case["expected_coupling_state"] not in VALID_COUPLING_STATES: raise AssertionError(f"{cid} has invalid expected_coupling_state.")
        for bf in ["claimed_classification","claimed_emission"]:
            if not isinstance(case[bf], bool): raise AssertionError(f"{cid}.{bf} must be boolean.")
        for f in NUMERIC_FIELDS: assert_unit_interval(f"{cid}.{f}", case[f])
def test_coupling_classification(payload: dict[str, Any]) -> None:
    for case in payload["cases"]:
        actual=classify_coupling(case,payload["compatibility_matrix"],payload["thresholds"]); expected=case["expected_coupling_state"]
        if actual != expected: raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}.")
def test_fixture_covers_required_coupling_states(payload: dict[str, Any]) -> None:
    seen={case["expected_coupling_state"] for case in payload["cases"]}; missing=sorted(VALID_COUPLING_STATES-seen)
    if missing: raise AssertionError(f"Fixture missing coupling states: {missing}")
def test_incompatible_observer_blocks_claims(payload: dict[str, Any]) -> None:
    for case in payload["cases"]:
        if not is_compatible(case,payload["compatibility_matrix"]):
            if case["expected_coupling_state"] != "incompatible_observer": raise AssertionError(f"{case['case_id']} incompatible observer was not blocked.")
def test_emittable_requires_compatible_observer(payload: dict[str, Any]) -> None:
    for case in payload["cases"]:
        if case["expected_coupling_state"] == "coupled_emittable":
            if not is_compatible(case,payload["compatibility_matrix"]): raise AssertionError(f"{case['case_id']} emitted without compatible observer.")
            if not case["claimed_emission"]: raise AssertionError(f"{case['case_id']} emittable case should claim emission.")
def main() -> None:
    payload=load_fixture()
    if not isinstance(payload.get("thresholds"),dict): raise AssertionError("Fixture must contain thresholds object.")
    if not isinstance(payload.get("cases"),list) or not payload["cases"]: raise AssertionError("Fixture must contain non-empty cases list.")
    validate_thresholds(payload["thresholds"]); validate_identity_model(payload); validate_cases(payload)
    test_fixture_covers_required_coupling_states(payload); test_coupling_classification(payload); test_incompatible_observer_blocks_claims(payload); test_emittable_requires_compatible_observer(payload)
    print("RTG observer-identity coupling tests passed.")
if __name__ == "__main__": main()
