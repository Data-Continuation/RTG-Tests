import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest_experiment_003_source.py"
RECEIPT = ROOT / "registry" / "experiment-003-dataset-selection-receipt.json"

spec = importlib.util.spec_from_file_location("rtg_exp003_ingest", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def run() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["selection_state"] == "LOCKED_BEFORE_ANALYSIS"
    assert len(receipt["files"]) == 6
    assert all(len(item["md5"]) == 32 for item in receipt["files"])

    sample = b"\xef\xbb\xbf# header\r\n  1   2  3 \r\n\r\n4\t5\t6\r\n"
    canonical = module.canonicalize_text(sample)
    assert canonical == "# header\n  1   2  3 \n\n4\t5\t6\n"
    assert module.data_rows(canonical) == ["1 2 3", "4 5 6"]

    key = "10.5281/zenodo.4953982\nFig2_Data.txt\n0\n1 2 3"
    first = module.partition_for_key(key)
    second = module.partition_for_key(key)
    assert first == second
    partition, bucket, digest = first
    assert partition in {"calibration", "validation", "locked_test"}
    assert 0 <= bucket <= 9
    assert len(digest) == 64

    assert module.digest_bytes(b"abc", "md5") == "900150983cd24fb0d6963f7d28e17f72"
    assert module.digest_bytes(b"abc", "sha256") == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )

    source = SCRIPT.read_text(encoding="utf-8")
    required_safety_terms = [
        '"outcome_statistics_computed": False',
        '"rtg_parameters_fitted": False',
        '"baseline_parameters_fitted": False',
        '"locked_test_content_exposed": False',
        '"partition_reassignment_allowed": False',
    ]
    for term in required_safety_terms:
        assert term in source, term

    print("RTG Experiment 003 integrity-ingestion unit tests passed.")


if __name__ == "__main__":
    run()
