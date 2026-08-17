import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/state-manifold-governance/core-cases.json"


def cases():
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0.0"
    return {case["id"]: case for case in data["cases"]}


class StateManifoldGovernanceAlignmentTests(unittest.TestCase):
    def test_snapshots_do_not_create_causal_edges(self):
        case = cases()["two-snapshots-no-edge"]
        self.assertEqual(case["observed_causal_edges"], [])
        self.assertEqual(case["expected_continuity_edges"], [])

    def test_refinement_preserves_established_coarse_edge(self):
        case = cases()["coarse-edge-refined"]
        self.assertIn(["a", "d"], case["observed_causal_edges"])
        self.assertIs(case["expected_coarse_edge_preserved"], True)
        self.assertEqual(len(case["refined_edges"]), 3)

    def test_higher_order_restriction_does_not_erase_causality(self):
        case = cases()["higher-order-deny-does-not-erase-edge"]
        self.assertEqual(case["governance"]["result"], "INADMISSIBLE")
        self.assertIs(case["expected_edge_preserved"], True)
        self.assertIs(case["expected_first_order_realizable"], True)

    def test_no_default_trajectory_taint(self):
        case = cases()["trajectory-no-default-taint"]
        self.assertIs(case["lineage_rule_present"], False)
        self.assertEqual(case["trajectory"][1]["governance"], "INADMISSIBLE")
        self.assertEqual(case["trajectory"][2]["governance"], "ADMISSIBLE")
        self.assertIs(case["expected_last_transition_admissible"], True)

    def test_classification_without_causal_intervention_is_not_enforcement(self):
        case = cases()["deny-without-intervention"]
        self.assertEqual(case["governance_classification"], "DENY")
        self.assertIsNone(case["causal_intervention_edge"])
        self.assertIs(case["expected_enforcement"], False)


if __name__ == "__main__":
    unittest.main()
