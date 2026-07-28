import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "evaluate_experiment_003_object_readiness.py"
spec = importlib.util.spec_from_file_location("object_readiness", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def manifest(objects):
    counts = {name: sum(obj["partition"] == name for obj in objects) for name in ("calibration", "validation", "locked_test")}
    return {
        "manifest_id": "m",
        "manifest_sha256": "a" * 64,
        "experiment_id": "RTG-EXP-003",
        "partition_unit": "publisher_aligned_experimental_observation",
        "partition_counts": counts,
        "objects": objects,
        "locks": {"locked_test_content_exposed": False},
    }


def obj(unit, partition):
    locked = partition == "locked_test"
    return {
        "analysis_unit": unit,
        "partition": partition,
        "sealed": locked,
        "values": None if locked else {"predictor": 1, "target": 0.8},
    }


def test_ready_requires_both_visible_partitions_for_each_unit():
    objects = []
    for unit in ("fig3_experimental_fidelity", "fig4_experimental_fidelity"):
        objects.extend([obj(unit, "calibration"), obj(unit, "calibration"), obj(unit, "validation")])
    receipt = module.evaluate(manifest(objects))
    assert receipt["state"] == "READY_FOR_CALIBRATION_FIT"
    assert receipt["stop_reasons"] == []
    assert receipt["visible_object_coverage"] == 1.0
    assert receipt["locked_test_content_opened"] is False
    assert receipt["model_fit_performed"] is False


def test_missing_unit_validation_stops():
    objects = [
        obj("fig3_experimental_fidelity", "calibration"),
        obj("fig3_experimental_fidelity", "validation"),
        obj("fig4_experimental_fidelity", "calibration"),
        obj("fig4_experimental_fidelity", "locked_test"),
    ]
    receipt = module.evaluate(manifest(objects))
    assert receipt["state"] == "STOP_REQUIRED"
    assert "NO_VALIDATION_OBJECTS_FOR_FIG4_EXPERIMENTAL_FIDELITY" in receipt["stop_reasons"]


def test_unsealed_locked_test_is_rejected():
    bad = obj("fig3_experimental_fidelity", "locked_test")
    bad["values"] = {"target": 0.8}
    try:
        module.evaluate(manifest([bad]))
    except ValueError as exc:
        assert "not sealed" in str(exc)
    else:
        raise AssertionError("unsealed locked-test object was accepted")
