import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "build_experiment_003_object_manifest.py"
SPLIT_PATH = ROOT / "registries" / "experiment-003-composite-object-split.json"

spec = importlib.util.spec_from_file_location("object_manifest", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_partition_assignment_is_deterministic_and_complete():
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    first = module.partition_for_object("object-001", split)
    second = module.partition_for_object("object-001", split)
    assert first == second
    partition, bucket, digest = first
    assert partition in {"calibration", "validation", "locked_test"}
    assert 0 <= bucket <= 99
    assert len(digest) == 64


def test_figure3_alignment_preserves_tuple_components():
    text = """
    nbar = {0.1, 0.2}
    expfidelity = {80, 70}
    errornbar={0.01, 0.02}
    errorsexpfidelity = {2, 3}
    theorynbar = {0.0, 1.0}
    theoryfidelity = {99, 99}
    """
    objects = module.figure3_objects(text)
    assert len(objects) == 2
    assert objects[0] == {
        "analysis_unit": "fig3_experimental_fidelity",
        "element_index": 0,
        "predictor_name": "mean_photon_number",
        "predictor": 0.1,
        "target": 0.8,
        "predictor_error": 0.01,
        "target_error": 0.02,
    }
    assert all("theory" not in json.dumps(obj).lower() for obj in objects)


def test_figure4_excludes_simulated_curve():
    text = """
    Data points, {tau, teleportation fidelity in percent}
    {{0, 75+-2}, {1, 65+-3}}
    Simulated blue theory curve
    {{0, 99}, {1, 99}}
    """
    objects = module.figure4_objects(text)
    assert len(objects) == 2
    assert objects[1]["predictor"] == 1.0
    assert objects[1]["target"] == 0.65
    assert objects[1]["target_error"] == 0.03


def test_locked_objects_are_sealed_without_value_fields(monkeypatch, tmp_path):
    receipt = {
        "receipt_id": "r",
        "source": {"record_doi": "10.5281/zenodo.4953982"},
        "files": [
            {"name": "Fig3_Data.txt", "md5": "x", "bytes": 1},
            {"name": "Fig4_Data.txt", "md5": "x", "bytes": 1},
        ],
    }
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    fig3 = b"nbar={0.1}\nexpfidelity={80}\nerrornbar={0.01}\nerrorsexpfidelity={2}\n"
    fig4 = b"Data points, {tau, teleportation fidelity in percent}\n{{0,75+-2}}\n"
    receipt["files"][0].update(md5=__import__("hashlib").md5(fig3).hexdigest(), bytes=len(fig3))
    receipt["files"][1].update(md5=__import__("hashlib").md5(fig4).hexdigest(), bytes=len(fig4))
    payloads = iter([fig3, fig4])
    monkeypatch.setattr(module, "retrieve", lambda _: next(payloads))
    monkeypatch.setattr(module, "partition_for_object", lambda object_id, split: ("locked_test", 90, "a" * 64))
    manifest = module.build_manifest(receipt, split, tmp_path)
    assert manifest["partition_counts"] == {"calibration": 0, "validation": 0, "locked_test": 2}
    assert all(obj["sealed"] is True and obj["values"] is None for obj in manifest["objects"])
    assert manifest["locks"]["locked_test_content_exposed"] is False
    assert manifest["locks"]["model_fit_performed"] is False
