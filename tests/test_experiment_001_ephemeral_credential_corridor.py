import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "experiment-001-ephemeral-credential-corridor.json"


def evaluate_case(case: dict) -> dict:
    operator_instantiated = (
        case["destination_requires_review"]
        and case["delta_hb"] >= case["threshold_hb"]
        and case["necessity"] >= case["threshold_necessity"]
    )

    decision = "NONE"
    ingested = False
    operator_expired = False

    if operator_instantiated:
        all_admissible = all(
            [
                case["credential_valid"],
                case["authority_valid"],
                case["freshness_valid"],
                case["destination_identity_valid"],
            ]
        )
        decision = "ALLOW" if all_admissible else "DENY"
        # Both ALLOW and DENY are decision payloads. Transport closes only
        # after the destination ingests that payload.
        ingested = True
        operator_expired = ingested

    # Every case must produce a terminal monitoring record, including the
    # bounded non-instantiation cases.
    closure_recorded = True

    return {
        "operator_instantiated": operator_instantiated,
        "decision": decision,
        "ingested": ingested,
        "operator_expired": operator_expired,
        "closure_recorded": closure_recorded,
        "null_triggered": case["destination_requires_review"],
    }


def run() -> None:
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert document["experiment_id"] == "RTG-EXP-001"
    assert document["posture"] == "falsifiable-computational-only"
    assert len(document["cases"]) >= 5

    differences_from_null = 0

    for case in document["cases"]:
        for bounded in ("delta_hb", "necessity", "threshold_hb", "threshold_necessity"):
            assert 0.0 <= case[bounded] <= 1.0, (case["event_id"], bounded)

        actual = evaluate_case(case)
        assert actual == case["expected"], {
            "event_id": case["event_id"],
            "actual": actual,
            "expected": case["expected"],
        }

        if actual["operator_instantiated"] != actual["null_triggered"]:
            differences_from_null += 1

        if actual["operator_instantiated"]:
            assert actual["decision"] in {"ALLOW", "DENY"}
            assert actual["ingested"] is True
            assert actual["operator_expired"] is True
        else:
            assert actual["decision"] == "NONE"
            assert actual["ingested"] is False

        assert actual["closure_recorded"] is True

    # The fixture suite must contain cases where RTG and the ordinary
    # event-trigger null model make different activation predictions.
    # This does not prove RTG; it makes the proposed distinction testable.
    assert differences_from_null >= 2

    print("RTG Experiment 001 ephemeral credential corridor tests passed.")
    print(f"cases={len(document['cases'])}")
    print(f"activation_differences_from_null={differences_from_null}")


if __name__ == "__main__":
    run()
