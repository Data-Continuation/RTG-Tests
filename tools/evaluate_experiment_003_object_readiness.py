#!/usr/bin/env python3
"""Evaluate whether the corrected Experiment 003 object manifest may advance.

This gate checks partition adequacy and visible-object coverage only. It does not
compute outcome statistics, inspect locked-test values, or fit any model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "results" / "experiment-003-object-manifest.json"
DEFAULT_OUTPUT = ROOT / "results" / "experiment-003-object-readiness.json"


def evaluate(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest["partition_unit"] != "publisher_aligned_experimental_observation":
        raise ValueError("unexpected partition unit")
    if manifest["locks"]["locked_test_content_exposed"]:
        raise ValueError("locked-test content exposure declared")
    objects = manifest["objects"]
    if not objects:
        raise ValueError("object manifest is empty")
    for obj in objects:
        if obj["partition"] == "locked_test":
            if obj.get("values") is not None or obj.get("sealed") is not True:
                raise ValueError("locked-test object is not sealed")
        elif obj["partition"] in {"calibration", "validation"}:
            if obj.get("values") is None or obj.get("sealed") is not False:
                raise ValueError("visible object is unexpectedly sealed")
        else:
            raise ValueError(f"unexpected partition: {obj['partition']}")

    counts = manifest["partition_counts"]
    visible = counts["calibration"] + counts["validation"]
    coverage = visible / len(objects)
    unit_counts = {
        unit: {
            partition: sum(1 for obj in objects if obj["analysis_unit"] == unit and obj["partition"] == partition)
            for partition in ("calibration", "validation", "locked_test")
        }
        for unit in sorted({obj["analysis_unit"] for obj in objects})
    }
    reasons: list[str] = []
    if counts["calibration"] == 0:
        reasons.append("NO_CALIBRATION_OBJECTS")
    if counts["validation"] == 0:
        reasons.append("NO_VALIDATION_OBJECTS")
    if coverage < 0.70:
        reasons.append("VISIBLE_OBJECT_COVERAGE_BELOW_0_70")
    for unit, by_partition in unit_counts.items():
        if by_partition["calibration"] == 0:
            reasons.append(f"NO_CALIBRATION_OBJECTS_FOR_{unit.upper()}")
        if by_partition["validation"] == 0:
            reasons.append(f"NO_VALIDATION_OBJECTS_FOR_{unit.upper()}")

    state = "READY_FOR_CALIBRATION_FIT" if not reasons else "STOP_REQUIRED"
    core = {
        "receipt_id": "RTG-EXP-003-OBJECT-READINESS-001",
        "experiment_id": manifest["experiment_id"],
        "manifest_id": manifest["manifest_id"],
        "manifest_sha256": manifest["manifest_sha256"],
        "state": state,
        "partition_counts": counts,
        "analysis_unit_partition_counts": unit_counts,
        "visible_object_coverage": coverage,
        "minimum_visible_object_coverage": 0.70,
        "stop_reasons": reasons,
        "locked_test_content_opened": False,
        "outcome_statistics_computed": False,
        "model_fit_performed": False,
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["receipt_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return core


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    receipt = evaluate(manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"state={receipt['state']}")
    print(f"visible_object_coverage={receipt['visible_object_coverage']:.6f}")
    print("stop_reasons=" + json.dumps(receipt["stop_reasons"]))
    print("locked_test_content_opened=false")
    print("model_fit_performed=false")


if __name__ == "__main__":
    main()
