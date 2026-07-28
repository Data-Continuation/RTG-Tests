#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "extract_experiment_003_publisher_schema.py"


def main() -> None:
    text = TOOL.read_text(encoding="utf-8")
    required = [
        "_Description.txt",
        "checksum mismatch",
        "byte-size mismatch",
        '"data_files_opened": False',
        '"outcome_statistics_computed": False',
        '"model_fit_performed": False',
        '"locked_test_opened": False',
        "HUMAN_REVIEW_REQUIRED_BEFORE_EXECUTABLE_SCHEMA_LOCK",
    ]
    missing = [token for token in required if token not in text]
    if missing:
        raise AssertionError(f"publisher schema extraction protections missing: {missing}")
    print("RTG Experiment 003 publisher schema extraction contract passed.")


if __name__ == "__main__":
    main()
