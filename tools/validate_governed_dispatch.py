#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

EXPECTED_REPOSITORY = "Data-Continuation/RTG-Tests"
EXPECTED_CAPABILITY = "governed_research_execution"


def canonical(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def validate(envelope: dict[str, Any]) -> dict[str, Any]:
    required = {"work_id", "destination", "authority_class", "contract_sha256", "envelope_sha256"}
    missing = sorted(required - envelope.keys())
    if missing:
        raise ValueError(f"missing dispatch fields: {missing}")
    if envelope["destination"]["repository"] != EXPECTED_REPOSITORY:
        raise ValueError("dispatch destination repository mismatch")
    if envelope["destination"]["capability"] != EXPECTED_CAPABILITY:
        raise ValueError("dispatch capability mismatch")
    if not envelope["work_id"].startswith("SV-WORK-RTG-EXP-003"):
        raise ValueError("dispatch work ID is outside Experiment 003 scope")
    core = {k: v for k, v in envelope.items() if k != "envelope_sha256"}
    digest = hashlib.sha256(canonical(core).encode("utf-8")).hexdigest()
    if digest != envelope["envelope_sha256"]:
        raise ValueError("dispatch envelope digest mismatch")
    return {
        "work_id": envelope["work_id"],
        "destination_repository": EXPECTED_REPOSITORY,
        "capability": EXPECTED_CAPABILITY,
        "dispatch_admissible": True,
        "contract_sha256": envelope["contract_sha256"],
        "envelope_sha256": envelope["envelope_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("envelope", type=Path)
    parser.add_argument("--receipt", type=Path, default=Path("results/experiment-003-dispatch-acceptance.json"))
    args = parser.parse_args()
    envelope = json.loads(args.envelope.read_text(encoding="utf-8"))
    receipt = validate(envelope)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
