import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries" / "experiment-003-composite-object-split.json"


def test_composite_split_is_locked_and_fail_closed():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert data["state"] == "LOCKED_BEFORE_COMPOSITE_ASSIGNMENT"
    assert data["partition_unit"] == "composite_analysis_object"
    assert data["superseded_manifest_retained"] is True
    assert data["locks"]["locked_test_content_opened"] is False
    assert data["locks"]["model_fit_performed"] is False
    assert data["locks"]["outcome_statistics_computed"] is False
    assert data["locks"]["superseded_split_may_be_reused_for_fitting"] is False


def test_fig3_components_cannot_receive_independent_partitions():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    fig3 = next(obj for obj in data["objects"] if obj["object_id"] == "fig3_experimental_series")
    assert set(fig3["required_records"]) == {
        "nbar",
        "expfidelity",
        "errornbar",
        "errorsexpfidelity",
    }
    assert "one shared partition" in fig3["assignment_rule"]


def test_allocation_is_deterministic_and_not_rebalanced():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    allocation = data["allocation"]
    assert allocation["method"] == "sha256_mod_100"
    assert allocation["calibration_buckets"] == [0, 59]
    assert allocation["validation_buckets"] == [60, 79]
    assert allocation["locked_test_buckets"] == [80, 99]
    assert allocation["retries_or_rebalancing"] is False
