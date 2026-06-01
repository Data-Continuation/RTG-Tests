# RTG Risk Pressure Decay Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **risk pressure decay semantic behavior**.

## Mechanism Group

```text
risk
```

## Done State

```text
fixtures/risk-pressure-decay-semantic-behavior.valid.json exists
tests/test_risk_pressure_decay_semantic_behavior.py exists
config/rtg_declared_tasks.json declares risk_pressure_decay_semantic_behavior_tests
python tests/test_risk_pressure_decay_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task risk_pressure_decay_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
