import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "registries" / "experiment-003-calibration-readiness.json"
CONTRACT = ROOT / "registries" / "experiment-003-calibration-contract.json"
MAPPING = ROOT / "registries" / "experiment-003-semantic-mapping.json"


def run() -> None:
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))

    assert readiness["experiment_id"] == contract["experiment_id"] == mapping["experiment_id"]
    assert readiness["state"] == "STOP_REQUIRED"
    assert readiness["locked_test_opened"] is False
    assert readiness["model_fit_performed"] is False
    assert "required_baseline_unconstructable" in readiness["governance_basis"]
    assert contract["state"] == "LOCKED_BEFORE_MODEL_FIT"
    assert mapping["state"] == "LOCKED_BEFORE_MODEL_FIT"
    assert "locked_test" in contract["forbidden_partitions"]

    required = set(readiness["required_before_fit"])
    assert any("exact ordered column schema" in item for item in required)
    assert any("prediction target" in item for item in required)
    assert any("deterministic transforms" in item for item in required)

    assert all(value is False for value in readiness["claims"].values())
    print("RTG Experiment 003 calibration readiness gate passed: STOP_REQUIRED.")


if __name__ == "__main__":
    run()
