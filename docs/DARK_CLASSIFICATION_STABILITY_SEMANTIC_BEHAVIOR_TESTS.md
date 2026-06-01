# RTG Dark Classification Stability Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **dark classification stability semantic behavior**.

## Mechanism Group

```text
dark
```

## Done State

```text
fixtures/dark-classification-stability-semantic-behavior.valid.json exists
tests/test_dark_classification_stability_semantic_behavior.py exists
config/rtg_declared_tasks.json declares dark_classification_stability_semantic_behavior_tests
python tests/test_dark_classification_stability_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task dark_classification_stability_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
