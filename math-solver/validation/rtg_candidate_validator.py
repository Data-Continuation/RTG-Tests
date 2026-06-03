#!/usr/bin/env python3
"""
rtg_candidate_validator.py

Deterministic RTG governance validator. This is the RTG-side counterpart to
gcat_bcat_candidate_validator.py. It does NOT do simplex/legitimacy math —
RTG vectors are boolean/null governance conditions, not numeric states.

It maps each candidate vector's governance conditions to one of:
    ALLOW_candidate | DENY_candidate | DEFER_candidate | REPLAY_candidate

and checks the result against the vector's declared expected_posture.

This mirrors the GCAT/BCAT validator's CLI so the workflow can route to it:
    python rtg_candidate_validator.py \
        --vectors <dir-or-file> \
        --out <report.json> \
        --summary-md <summary.md>

No network. No API. Pure deterministic governance evaluation.
Claim boundary preserved: this produces CANDIDATE postures, never verified proofs.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

ALLOW = "ALLOW_candidate"
DENY = "DENY_candidate"
DEFER = "DEFER_candidate"
REPLAY = "REPLAY_candidate"
FAIL_CLOSED = "FAIL_CLOSED"


def classify(vector: Dict[str, Any]) -> Tuple[str, str]:
    """Return (posture, reason) for one RTG candidate vector.

    The RTG governance gate, encoded deterministically:
      - A replay/round-trip candidate is checked for round-trip completeness.
      - A transition candidate's chain must not collapse:
          claim_boundary_preserved == False  -> false_transition -> DENY
          observer_detector_match  == False  -> false_transition -> DENY
          observer_detector_match  == None   -> unknown_unknown   -> DEFER
          all gates True                      -> ALLOW
      - Missing required governance keys -> FAIL_CLOSED (cannot govern blindly).
    """
    cls = vector.get("class")
    conds = vector.get("conditions", {})
    if not isinstance(conds, dict):
        return FAIL_CLOSED, "conditions_block_invalid"

    # Round-trip / replay candidates have a different condition surface.
    if cls == "repeatable_round_trip_candidate":
        required = (
            "instruction_artifact_present",
            "upload_manifest_present",
            "returned_artifact_ingestion_required",
            "next_instruction_required",
        )
        for k in required:
            if k not in conds:
                return FAIL_CLOSED, f"replay_condition_missing_{k}"
        if all(bool(conds[k]) for k in required):
            return REPLAY, "round_trip_complete"
        return DEFER, "round_trip_incomplete"

    # Transition candidates: governance chain must not collapse.
    required = (
        "authority_bound",
        "claim_boundary_preserved",
        "cost_status_receipted",
        "observer_detector_match",
        "publication_gate_required",
    )
    for k in required:
        if k not in conds:
            return FAIL_CLOSED, f"condition_missing_{k}"

    # Authority is a hard gate.
    if conds["authority_bound"] is not True:
        return DENY, "authority_unbound"

    # unknown_unknown: detector match is explicitly null (not observed) ->
    # defer / preserve anomaly, do NOT treat as fraud.
    if conds["observer_detector_match"] is None:
        return DEFER, "unknown_unknown_detector_null"

    # false_transition: claim boundary broken or detector mismatch -> DENY.
    if conds["claim_boundary_preserved"] is not True:
        return DENY, "claim_boundary_violated"
    if conds["observer_detector_match"] is not True:
        return DENY, "observer_detector_mismatch"

    # All gates satisfied -> ALLOW candidate (not a verified proof).
    if conds["cost_status_receipted"] is not True:
        return DENY, "cost_status_unreceipted"
    return ALLOW, "rtg_admissible_candidate"


def validate_payload(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    results = []
    for v in payload.get("candidate_vectors", []):
        posture, reason = classify(v)
        expected = v.get("expected_posture")
        passed = expected is not None and posture == expected
        results.append({
            "vector_id": v.get("vector_id"),
            "class": v.get("class"),
            "expected_posture": expected,
            "actual_posture": posture,
            "reason": reason,
            "passed": passed,
        })
    return results


def gather_payloads(path: Path) -> List[Path]:
    if path.is_file():
        return [path]
    return sorted(path.glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vectors", required=True,
                        help="RTG candidate vectors file or directory")
    parser.add_argument("--out", required=True)
    parser.add_argument("--summary-md", default=None)
    args = parser.parse_args()

    vpath = Path(args.vectors)
    all_results: List[Dict[str, Any]] = []
    claim_boundary = None

    for p in gather_payloads(vpath):
        try:
            payload = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            all_results.append({
                "vector_id": p.stem, "class": None,
                "expected_posture": None, "actual_posture": FAIL_CLOSED,
                "reason": f"malformed_json:{exc}", "passed": False,
            })
            continue
        if claim_boundary is None:
            claim_boundary = payload.get("claim_boundary")
        all_results.extend(validate_payload(payload))

    total = len(all_results)
    passed = sum(1 for r in all_results if r["passed"])
    report = {
        "validator": "rtg_candidate_validator",
        "schema_version": "1.0",
        "total_vectors": total,
        "passed": passed,
        "failed": total - passed,
        "all_passed": total > 0 and passed == total,
        "claim_boundary": claim_boundary,
        "results": all_results,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")

    if args.summary_md:
        lines = [
            "## RTG Candidate Validation",
            "",
            f"- Total vectors: **{total}**",
            f"- Passed: **{passed}**",
            f"- Failed: **{total - passed}**",
            f"- All passed: **{report['all_passed']}**",
            "",
            "| Vector | Class | Expected | Actual | Reason | Pass |",
            "|---|---|---|---|---|---|",
        ]
        for r in all_results:
            lines.append(
                f"| {r['vector_id']} | {r.get('class')} | "
                f"{r['expected_posture']} | {r['actual_posture']} | "
                f"{r['reason']} | {'✅' if r['passed'] else '❌'} |"
            )
        Path(args.summary_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.summary_md).write_text("\n".join(lines) + "\n",
                                         encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
