# RTG Confidence Source Drift Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **confidence source drift semantic behavior**.

## Mechanism Group

```text
confidence
```

## Done State

```text
fixtures/confidence-source-drift-semantic-behavior.valid.json exists
tests/test_confidence_source_drift_semantic_behavior.py exists
config/rtg_declared_tasks.json declares confidence_source_drift_semantic_behavior_tests
python tests/test_confidence_source_drift_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task confidence_source_drift_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
