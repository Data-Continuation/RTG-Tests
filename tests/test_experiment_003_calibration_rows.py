import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "prepare_experiment_003_calibration_rows.py"
SCHEMA_PATH = ROOT / "registries" / "experiment-003-executable-source-schema.json"

spec = importlib.util.spec_from_file_location("prepare_exp003", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def base_manifest(rows):
    return {
        "manifest_id": "RTG-EXP-003-SEALED-SPLIT-001",
        "locks": {"locked_test_content_exposed": False},
        "rows": rows,
    }


def row(file_name, index, partition, text):
    return {
        "file_name": file_name,
        "zero_based_data_row_index": index,
        "partition": partition,
        "canonical_row_text": text,
        "canonical_row_sha256": f"hash-{file_name}-{index}",
    }


def test_parser_expands_only_allowed_partitions_and_keeps_test_sealed():
    rows = [
        row("Fig3_Data.txt", 0, "calibration", "nbar = {0.1, 0.2}"),
        row("Fig3_Data.txt", 1, "calibration", "expfidelity = {80, 70}"),
        row("Fig3_Data.txt", 2, "calibration", "errornbar={0.01, 0.02}"),
        row("Fig3_Data.txt", 3, "calibration", "errorsexpfidelity = {2, 3}"),
        row("Fig4_Data.txt", 0, "validation", "{{0, 75+-2}, {1, 65+-3}}"),
        row("Fig4_Data.txt", 1, "locked_test", None),
    ]
    receipt = module.prepare(base_manifest(rows), schema())
    assert receipt["record_counts"] == {"calibration": 2, "validation": 2}
    assert receipt["locked_test_content_opened"] is False
    assert receipt["model_fit_performed"] is False
    assert all(record["partition"] != "locked_test" for record in receipt["records"])
    assert receipt["records"][0]["target"] == 0.8


def test_locked_test_content_exposure_is_rejected():
    rows = [row("Fig4_Data.txt", 0, "locked_test", "{{0, 75+-2}}")]
    try:
        module.prepare(base_manifest(rows), schema())
    except ValueError as exc:
        assert "locked-test row content exposed" in str(exc)
    else:
        raise AssertionError("locked-test exposure was not rejected")


def test_incomplete_fig3_partition_does_not_cross_partition_join():
    rows = [
        row("Fig3_Data.txt", 0, "calibration", "nbar = {0.1}"),
        row("Fig3_Data.txt", 1, "validation", "expfidelity = {80}"),
        row("Fig3_Data.txt", 2, "calibration", "errornbar={0.01}"),
        row("Fig3_Data.txt", 3, "validation", "errorsexpfidelity = {2}"),
    ]
    receipt = module.prepare(base_manifest(rows), schema())
    assert receipt["records"] == []
    assert receipt["state"] == "STOP_REQUIRED"
