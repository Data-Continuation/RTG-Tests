#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "registries" / "experiment-003-executable-source-schema.json"


def main() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["state"] == "LOCKED_BEFORE_OUTCOME_STATISTICS_OR_MODEL_FIT"
    assert schema["evidence"]["locked_test_opened"] is False
    rules = schema["global_rules"]
    assert rules["prediction_target"] == "teleportation_fidelity"
    assert rules["validation_may_select_parameters"] is False
    assert rules["locked_test_access"] is False
    assert rules["outcome_statistics_computed"] is False
    assert rules["model_fit_performed"] is False

    units = {u["unit_id"]: u for u in schema["analysis_units"]}
    assert units["fig3_experimental_fidelity"]["include"] is True
    assert units["fig4_experimental_fidelity"]["include"] is True
    assert units["fig2_density_matrices_and_summary_fidelities"]["include"] is False

    for unit_id in ("fig3_experimental_fidelity", "fig4_experimental_fidelity"):
        columns = units[unit_id]["columns"]
        targets = [c for c in columns if c["role"] == "prediction_target"]
        assert len(targets) == 1
        assert targets[0]["name"] == "teleportation_fidelity"
        assert targets[0]["transform"] == "divide_by_100"

    assert "theorynbar" in units["fig3_experimental_fidelity"]["excluded_records"]
    assert "Simulated blue theory curve" in units["fig4_experimental_fidelity"]["excluded_records"]
    print("RTG Experiment 003 executable source schema passed.")


if __name__ == "__main__":
    main()
