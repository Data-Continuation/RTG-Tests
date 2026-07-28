import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries" / "experiment-003-composite-object-split.json"


def test_composite_split_is_locked_and_fail_closed():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["state"] == "LOCKED_BEFORE_COMPOSITE_ASSIGNMENT"
    assert data["partition_unit"] == "composite_observation_object"
    assert data["superseded_manifest_retained"] is True
    assert data["locks"]["locked_test_content_opened_after_assignment"] is False
    assert data["locks"]["model_fit_performed"] is False
    assert data["locks"]["outcome_statistics_computed"] is False
    assert data["locks"]["superseded_split_may_be_reused_for_fitting"] is False


def test_fig3_components_cannot_receive_independent_partitions():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    fig3 = next(
        obj for obj in data["object_construction"]
        if obj["object_class"] == "fig3_experimental_observation"
    )
    assert set(fig3["required_records"]) == {
        "nbar",
        "expfidelity",
        "errornbar",
        "errorsexpfidelity",
    }
    assert fig3["alignment"] == "same_zero_based_element_index"
    assert "each aligned four-field tuple" in fig3["assignment_rule"]


def test_each_fig4_pair_is_one_partition_unit():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    fig4 = next(
        obj for obj in data["object_construction"]
        if obj["object_class"] == "fig4_experimental_observation"
    )
    assert fig4["alignment"] == "one published experimental pair"
    assert "each experimental pair" in fig4["assignment_rule"]


def test_allocation_is_deterministic_and_not_rebalanced():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    allocation = data["allocation"]
    assert allocation["method"] == "sha256_mod_100"
    assert allocation["calibration_buckets"] == [0, 59]
    assert allocation["validation_buckets"] == [60, 79]
    assert allocation["locked_test_buckets"] == [80, 99]
    assert allocation["retries_or_rebalancing"] is False
    assert data["object_identity"]["hash"] == "sha256"
