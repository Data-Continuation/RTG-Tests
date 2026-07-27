import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "registry" / "experiment-003-dataset-selection-receipt.json"


def run() -> None:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))

    assert data["receipt_id"] == "RTG-EXP-003-DATASET-001"
    assert data["experiment_id"] == "RTG-EXP-003"
    assert data["selection_state"] == "LOCKED_BEFORE_ANALYSIS"

    source = data["source"]
    assert source["record_doi"] == "10.5281/zenodo.4953982"
    assert source["license"] == "CC-BY-4.0"
    assert source["version"] == "v1"

    files = data["files"]
    assert len(files) == 6
    assert len({item["name"] for item in files}) == len(files)
    for item in files:
        assert item["bytes"] > 0
        assert len(item["md5"]) == 32
        int(item["md5"], 16)

    split = data["split"]
    assert split["method"] == "sha256-row-assignment-v1"
    buckets = (
        split["calibration_buckets"]
        + split["validation_buckets"]
        + split["locked_test_buckets"]
    )
    assert sorted(buckets) == list(range(10))
    assert len(set(buckets)) == 10
    assert split["target_proportions"] == {
        "calibration": 0.6,
        "validation": 0.2,
        "locked_test": 0.2,
    }
    assert split["outcome_dependent_reassignment_allowed"] is False

    lock = data["analysis_lock"]
    assert lock["data_downloaded_before_receipt"] is False
    assert lock["outcomes_inspected_before_selection"] is False
    assert lock["rtg_parameters_may_use_locked_test"] is False
    assert lock["baseline_parameters_may_use_locked_test"] is False

    assert all(value is False for value in data["claims"].values())

    print("RTG Experiment 003 dataset selection receipt passed.")
    print(f"files={len(files)}")
    print("split=60/20/20 deterministic hash assignment")
    print("selection_state=LOCKED_BEFORE_ANALYSIS")


if __name__ == "__main__":
    run()
