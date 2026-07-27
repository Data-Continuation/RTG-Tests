import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "experiment-002-distributed-heartbeat-surface.json"
OUTPUT = ROOT / "results" / "experiment-002-result.json"


def weighted_mismatch(components: dict, weights: dict) -> float:
    return sum(weights[name] * (components[name] ** 2) for name in weights)


def evaluate(case: dict, document: dict) -> dict:
    thresholds = document["thresholds"]
    mismatch = weighted_mismatch(case["components"], document["weights"])
    rtg_active = all(
        [
            case["transition_requested"],
            case["necessity"] >= thresholds["necessity"],
            mismatch >= thresholds["weighted_mismatch"],
            case["authority_valid"],
            case["lineage_valid"],
            case["route_available"],
        ]
    )
    return {
        "event_id": case["event_id"],
        "weighted_mismatch": round(mismatch, 6),
        "rtg_active": rtg_active,
        "decision": "ALLOW" if rtg_active and case["destination_ingests"] else "NONE",
        "operator_expired": rtg_active and case["destination_ingests"],
        "nulls": {
            "event": case["transition_requested"],
            "queue": case["queue_pressure"] >= thresholds["queue"],
            "scalar": max(case["components"].values()) >= thresholds["scalar_component"],
            "static_route": case["route_available"],
        },
    }


def run() -> None:
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    records = [evaluate(case, document) for case in document["cases"]]
    disagreements = {
        name: sum(record["rtg_active"] != record["nulls"][name] for record in records)
        for name in ("event", "queue", "scalar", "static_route")
    }
    exact_matches = 0
    for case, record in zip(document["cases"], records):
        expected = case["expected"]
        mapped = {
            "rtg_active": record["rtg_active"],
            "decision": record["decision"],
            "event_null": record["nulls"]["event"],
            "queue_null": record["nulls"]["queue"],
            "scalar_null": record["nulls"]["scalar"],
            "static_route_null": record["nulls"]["static_route"],
            "weighted_mismatch": record["weighted_mismatch"],
            "closure_recorded": True,
            "operator_expired": record["operator_expired"],
        }
        if all(mapped[key] == value for key, value in expected.items()):
            exact_matches += 1

    result = {
        "experiment_id": document["experiment_id"],
        "posture": document["posture"],
        "case_count": len(records),
        "exact_expected_matches": exact_matches,
        "null_disagreements": disagreements,
        "distinguishable_from_each_null": all(value >= 1 for value in disagreements.values()),
        "advancement_gate": "computational_distinguishability_only",
        "proof_claim": False,
        "physical_validation_claim": False,
        "quantum_claim": False,
        "records": records,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    print(f"exact_expected_matches={exact_matches}")
    for name, value in disagreements.items():
        print(f"disagreements_{name}={value}")


if __name__ == "__main__":
    run()
