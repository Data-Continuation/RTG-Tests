import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "experiment-002-distributed-heartbeat-surface.json"


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

    decision = "ALLOW" if rtg_active and case["destination_ingests"] else "NONE"

    return {
        "rtg_active": rtg_active,
        "decision": decision,
        "event_null": case["transition_requested"],
        "queue_null": case["queue_pressure"] >= thresholds["queue"],
        "scalar_null": max(case["components"].values()) >= thresholds["scalar_component"],
        "static_route_null": case["route_available"],
        "weighted_mismatch": round(mismatch, 6),
        "closure_recorded": True,
        "operator_expired": rtg_active and case["destination_ingests"],
    }


def run() -> None:
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert document["experiment_id"] == "RTG-EXP-002"
    assert document["posture"] == "falsifiable-computational-only"
    assert abs(sum(document["weights"].values()) - 1.0) < 1e-9
    assert len(document["cases"]) >= 6

    disagreements = {name: 0 for name in ("event_null", "queue_null", "scalar_null", "static_route_null")}

    for case in document["cases"]:
        for value in case["components"].values():
            assert 0.0 <= value <= 1.0
        assert 0.0 <= case["necessity"] <= 1.0
        assert 0.0 <= case["queue_pressure"] <= 1.0

        actual = evaluate(case, document)
        expected = case["expected"]
        for key, expected_value in expected.items():
            assert actual[key] == expected_value, {
                "event_id": case["event_id"],
                "field": key,
                "actual": actual[key],
                "expected": expected_value,
            }

        for null_name in disagreements:
            if actual["rtg_active"] != actual[null_name]:
                disagreements[null_name] += 1

        assert actual["closure_recorded"] is True
        if actual["rtg_active"]:
            assert actual["decision"] == "ALLOW"
            assert actual["operator_expired"] is True
        else:
            assert actual["decision"] == "NONE"
            assert actual["operator_expired"] is False

    # Each null model must disagree with the RTG candidate on at least one
    # preregistered case. This proves distinguishability, not superiority.
    assert all(count >= 1 for count in disagreements.values()), disagreements

    print("RTG Experiment 002 distributed heartbeat-surface tests passed.")
    print(f"cases={len(document['cases'])}")
    for name, count in disagreements.items():
        print(f"disagreements_{name}={count}")


if __name__ == "__main__":
    run()
