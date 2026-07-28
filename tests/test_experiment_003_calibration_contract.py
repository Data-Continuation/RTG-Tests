import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "registries" / "experiment-003-calibration-contract.json"


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert contract["experiment_id"] == "RTG-EXP-003"
    assert contract["state"] == "LOCKED_BEFORE_MODEL_FIT"
    assert contract["allowed_partitions"] == ["calibration", "validation"]
    assert contract["forbidden_partitions"] == ["locked_test"]
    assert contract["primary_metric"] == "mean_absolute_error"
    assert contract["minimum_mapping_coverage"] == 0.70
    assert contract["minimum_absolute_mae_improvement"] == 0.01

    candidate = contract["candidate"]
    assert candidate["fit_partition"] == "calibration"
    assert candidate["evaluation_partition"] == "validation"
    assert candidate["normalization_fit_partition"] == "calibration"
    assert candidate["may_use_validation_for_parameter_selection"] is False
    assert candidate["may_use_locked_test"] is False

    expected_baselines = {
        "constant_mean",
        "ordinary_least_squares",
        "ridge_regression",
        "isotonic_regression",
        "random_forest",
    }
    actual_baselines = {baseline["name"] for baseline in contract["baselines"]}
    assert actual_baselines == expected_baselines
    assert all(baseline["deterministic"] is True for baseline in contract["baselines"])

    rules = set(contract["stop_rules"])
    assert "partition_leakage_detected" in rules
    assert "locked_test_access_detected" in rules
    assert "mapping_coverage_below_0.70" in rules

    advancement = contract["advancement_rule"]
    assert advancement["beats_every_baseline"] is True
    assert advancement["closure_rate_must_not_decrease"] is True
    assert advancement["recoverability_rate_must_not_decrease"] is True

    assert not any(contract["claim_boundaries"].values())

    # Interface dry-run: demonstrate deterministic scoring and advancement logic
    # with synthetic values only. No experiment rows are opened here.
    candidate_mae = 0.10
    baseline_maes = {
        "constant_mean": 0.15,
        "ordinary_least_squares": 0.13,
        "ridge_regression": 0.12,
        "isotonic_regression": 0.14,
        "random_forest": 0.115,
    }
    margin = contract["minimum_absolute_mae_improvement"]
    advances = all(candidate_mae <= score - margin for score in baseline_maes.values())
    assert advances is True

    print("RTG Experiment 003 calibration contract validated.")
    print("locked_test_opened=false")
    print("model_fit_performed=false")
    print("synthetic_interface_dry_run=true")


if __name__ == "__main__":
    main()
