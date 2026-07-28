import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "registries" / "experiment-003-partition-unit-correction.json"


def test_partition_unit_correction_is_fail_closed_and_reconstructable():
    record = json.loads(CORRECTION.read_text(encoding="utf-8"))
    assert record["state"] == "STOPPED_BEFORE_MODEL_FIT"
    assert record["observed"]["mapping_coverage"] < record["observed"]["minimum_mapping_coverage"]
    assert record["observed"]["locked_test_content_opened"] is False
    assert record["observed"]["model_fit_performed"] is False
    assert record["required_correction"]["new_manifest_required"] is True
    assert record["required_correction"]["partition_assignment_unit"] == "publisher-defined composite analysis object before element expansion"
    assert set(record["required_correction"]["fig3_composite_members"]) == {
        "nbar", "expfidelity", "errornbar", "errorsexpfidelity"
    }
    assert "no reuse of the superseded split for fitting" in record["prohibitions"]
    assert "no deletion or rewriting of prior receipts" in record["prohibitions"]


def test_partition_buckets_are_complete_and_disjoint():
    record = json.loads(CORRECTION.read_text(encoding="utf-8"))
    buckets = record["required_correction"]["partition_buckets"]
    groups = [set(buckets[name]) for name in ("calibration", "validation", "locked_test")]
    assert set.union(*groups) == set(range(10))
    assert not (groups[0] & groups[1])
    assert not (groups[0] & groups[2])
    assert not (groups[1] & groups[2])
