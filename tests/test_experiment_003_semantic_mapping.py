import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries" / "experiment-003-semantic-mapping.json"


def run() -> None:
    doc = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert doc["experiment_id"] == "RTG-EXP-003"
    assert doc["state"] == "LOCKED_BEFORE_MODEL_FIT"
    assert doc["locked_test_access"] is False
    assert set(doc["allowed_partitions"]) == {"calibration", "validation"}

    observables = doc["rtg_observables"]
    names = {item["name"] for item in observables}
    assert names == {
        "phase_differential",
        "cadence_differential",
        "authority_differential",
        "lineage_differential",
        "route_differential",
        "destination_differential",
        "necessity",
        "weighted_mismatch",
        "closure",
        "recoverability",
    }
    assert all(item["range"] == [0.0, 1.0] for item in observables)

    missing = doc["missing_data"]
    assert "INDETERMINATE" in missing["rtg_activation"]
    assert missing["test-informed_rule_changes"] is False
    assert "forbidden" in missing["row_deletion"]

    baselines = doc["baseline_contracts"]
    assert len(baselines) == 5
    assert {b["class"] for b in baselines} == {
        "intercept-only",
        "linear",
        "regularized-linear",
        "monotone-nonlinear",
        "nonlinear-ensemble",
    }
    assert all("locked" not in b["fit"].lower() for b in baselines)

    scoring = doc["scoring"]
    assert scoring["primary"] == "mean_absolute_error"
    assert "every baseline" in scoring["advancement_rule"]
    assert "0.70" in scoring["stop_rule"]

    assert all(value is False for value in doc["claims"].values())
    print("RTG Experiment 003 semantic mapping registry validated.")


if __name__ == "__main__":
    run()
