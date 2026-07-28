import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "experiment-001-ephemeral-credential-corridor.json"
OUTPUT = ROOT / "results" / "experiment-001-results.json"


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
        admissible = all(
            case[key]
            for key in (
                "credential_valid",
                "authority_valid",
                "freshness_valid",
                "destination_identity_valid",
            )
        )
        decision = "ALLOW" if admissible else "DENY"
        ingested = True
        operator_expired = True
    return {
        "operator_instantiated": operator_instantiated,
        "decision": decision,
        "ingested": ingested,
        "operator_expired": operator_expired,
        "closure_recorded": True,
        "null_triggered": case["destination_requires_review"],
    }


def main() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    rows = []
    disagreements = 0
    exact_matches = 0
    for case in fixture["cases"]:
        observed = evaluate_case(case)
        matched = observed == case["expected"]
        exact_matches += int(matched)
        disagreements += int(observed["operator_instantiated"] != observed["null_triggered"])
        rows.append(
            {
                "event_id": case["event_id"],
                "delta_hb": case["delta_hb"],
                "necessity": case["necessity"],
                "rtg_operator_instantiated": observed["operator_instantiated"],
                "event_driven_null_triggered": observed["null_triggered"],
                "decision": observed["decision"],
                "expected_match": matched,
            }
        )

    result = {
        "experiment_id": fixture["experiment_id"],
        "posture": fixture["posture"],
        "case_count": len(rows),
        "expected_matches": exact_matches,
        "activation_differences_from_null": disagreements,
        "candidate_model_distinct_from_null_on_fixture": disagreements > 0,
        "proof_claim": False,
        "physical_validation_claim": False,
        "cases": rows,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
