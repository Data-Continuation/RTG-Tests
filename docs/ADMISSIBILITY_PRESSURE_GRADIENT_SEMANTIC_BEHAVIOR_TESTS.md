# RTG Admissibility Pressure Gradient Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **admissibility pressure gradient semantic behavior**.

## Mechanism Group

```text
admissibility
```

## Done State

```text
fixtures/admissibility-pressure-gradient-semantic-behavior.valid.json exists
tests/test_admissibility_pressure_gradient_semantic_behavior.py exists
config/rtg_declared_tasks.json declares admissibility_pressure_gradient_semantic_behavior_tests
python tests/test_admissibility_pressure_gradient_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task admissibility_pressure_gradient_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
