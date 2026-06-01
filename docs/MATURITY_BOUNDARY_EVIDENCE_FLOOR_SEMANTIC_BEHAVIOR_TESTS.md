# RTG Maturity Boundary Evidence Floor Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **maturity boundary evidence floor semantic behavior**.

## Mechanism Group

```text
maturity
```

## Done State

```text
fixtures/maturity-boundary-evidence-floor-semantic-behavior.valid.json exists
tests/test_maturity_boundary_evidence_floor_semantic_behavior.py exists
config/rtg_declared_tasks.json declares maturity_boundary_evidence_floor_semantic_behavior_tests
python tests/test_maturity_boundary_evidence_floor_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task maturity_boundary_evidence_floor_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
