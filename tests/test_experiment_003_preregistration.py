import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registries" / "experiment-003-preregistration.json"
DOC = ROOT / "docs" / "EXPERIMENT_003_QUANTUM_NETWORK_REINTERPRETATION.md"


def run() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    document = DOC.read_text(encoding="utf-8")

    assert registry["experiment_id"] == "RTG-EXP-003"
    assert registry["status"] == "preregistered"
    assert registry["maturity"] == "QUANTUM_REINTERPRETATION_REGISTERED"
    assert registry["dataset_selected"] is False
    assert registry["dataset_identifier"] is None
    assert registry["dataset_checksum"] is None

    assert len(registry["source_classes_allowed"]) == 4
    assert len(registry["locked_variables"]) == 10
    assert len(registry["required_baselines"]) >= 5
    assert len(registry["stop_conditions"]) >= 5

    splits = registry["split_constraints"]
    assert splits["training_max_fraction"] <= 0.60
    assert splits["validation_min_fraction"] >= 0.20
    assert splits["test_min_fraction"] >= 0.20
    assert splits["test_locked_before_evaluation"] is True
    assert (
        splits["training_max_fraction"]
        + splits["validation_min_fraction"]
        + splits["test_min_fraction"]
        <= 1.0
    )

    assert all(value is False for value in registry["claims"].values())

    required_document_terms = [
        "preregistered reinterpretation only",
        "locked test set",
        "Stop conditions",
        "Physical validation claim:** false",
        "Prohibited:",
        "instantaneous particle traversal",
        "faster-than-light signaling",
    ]
    for term in required_document_terms:
        assert term in document, term

    print("RTG Experiment 003 preregistration validation passed.")
    print("dataset_selected=false")
    print("physical_validation_claim=false")


if __name__ == "__main__":
    run()
