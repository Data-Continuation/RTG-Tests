import hashlib
import json

from tools.validate_governed_dispatch import canonical, validate


def envelope():
    core = {
        "work_id": "SV-WORK-RTG-EXP-003",
        "destination": {
            "entity": "DC",
            "repository": "Data-Continuation/RTG-Tests",
            "capability": "governed_research_execution",
        },
        "authority_class": "prepare",
        "contract_sha256": "a" * 64,
    }
    return {**core, "envelope_sha256": hashlib.sha256(canonical(core).encode()).hexdigest()}


def test_valid_dispatch_is_admitted():
    receipt = validate(envelope())
    assert receipt["dispatch_admissible"] is True


def test_wrong_destination_is_rejected():
    data = envelope()
    data["destination"]["repository"] = "other/repo"
    try:
        validate(data)
    except ValueError as exc:
        assert "destination repository mismatch" in str(exc)
    else:
        raise AssertionError("wrong destination was admitted")
