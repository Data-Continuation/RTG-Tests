import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/state-manifold-governance/core-cases.json"


def cases():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0.0"
    return {case["id"]: case for case in data["cases"]}


def test_snapshots_do_not_create_causal_edges():
    case = cases()["two-snapshots-no-edge"]
    assert case["observed_causal_edges"] == []
    assert case["expected_continuity_edges"] == []


def test_refinement_preserves_established_coarse_edge():
    case = cases()["coarse-edge-refined"]
    assert ["a", "d"] in case["observed_causal_edges"]
    assert case["expected_coarse_edge_preserved"] is True
    assert len(case["refined_edges"]) == 3


def test_higher_order_restriction_does_not_erase_causality():
    case = cases()["higher-order-deny-does-not-erase-edge"]
    assert case["governance"]["result"] == "INADMISSIBLE"
    assert case["expected_edge_preserved"] is True
    assert case["expected_first_order_realizable"] is True


def test_no_default_trajectory_taint():
    case = cases()["trajectory-no-default-taint"]
    assert case["lineage_rule_present"] is False
    assert case["trajectory"][1]["governance"] == "INADMISSIBLE"
    assert case["trajectory"][2]["governance"] == "ADMISSIBLE"
    assert case["expected_last_transition_admissible"] is True


def test_classification_without_causal_intervention_is_not_enforcement():
    case = cases()["deny-without-intervention"]
    assert case["governance_classification"] == "DENY"
    assert case["causal_intervention_edge"] is None
    assert case["expected_enforcement"] is False
