import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "multi-trajectory-field.example.json"
VALID_CLASSES = {"active", "supporting", "latent", "discardable"}


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def reclassify(score, threshold, coupled=False, latent_score=0.0):
    if score >= threshold:
        return "active"
    if coupled:
        return "supporting"
    if latent_score >= 0.7:
        return "latent"
    return "discardable"


def minimum_micro_nodes(graph_complexity, concurrency, uncertainty, authority_regimes):
    value = graph_complexity + concurrency + uncertainty + authority_regimes
    return max(1, int(value + 0.999999))


def test_fixture_has_all_significance_classes():
    data = load_fixture()
    assert {item["class"] for item in data["candidate_transitions"]} == VALID_CLASSES


def test_active_transitions_meet_context_threshold():
    data = load_fixture()
    threshold = data["context"]["significance_threshold"]
    active = [item for item in data["candidate_transitions"] if item["class"] == "active"]
    assert active and all(item["score"] >= threshold for item in active)


def test_latent_transition_can_be_promoted_after_deformation():
    data = load_fixture()
    latent = next(item for item in data["candidate_transitions"] if item["class"] == "latent")
    threshold = data["context"]["significance_threshold"]
    deformed_score = min(1.0, latent["score"] + data["geometry_deformation"]["magnitude"] * 0.25)
    assert latent["score"] < threshold <= deformed_score
    assert reclassify(deformed_score, threshold, coupled=True, latent_score=latent["score_components"]["latent"]) == "active"


def test_discardable_transition_is_uncoupled_and_low_latent():
    data = load_fixture()
    item = next(item for item in data["candidate_transitions"] if item["class"] == "discardable")
    assert item["coupled_transition_ids"] == []
    assert item["score_components"]["latent"] < 0.7


def test_reachable_state_probabilities_form_distribution():
    data = load_fixture()
    assert abs(sum(state["probability"] for state in data["reachable_state_frontier"]) - 1.0) < 1e-9


def test_irreversible_action_deforms_geometry():
    data = load_fixture()
    active = next(item for item in data["candidate_transitions"] if item["class"] == "active")
    deformation = data["geometry_deformation"]
    assert active["reversible"] is False
    assert deformation["magnitude"] > 0
    assert deformation["closed_state_ids"] or deformation["opened_state_ids"]


def test_micro_node_demand_tracks_topology_not_raw_count():
    simple_many = minimum_micro_nodes(1, 1, 0.1, 1)
    complex_few = minimum_micro_nodes(4, 3, 0.9, 4)
    assert complex_few > simple_many


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"RTG multi-trajectory tests passed: {len(tests)}")
