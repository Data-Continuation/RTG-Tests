# RTG Unknown External Perturbation Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **unknown external perturbation semantic behavior**.

## Mechanism Group

```text
unknown
```

## Done State

```text
fixtures/unknown-external-perturbation-semantic-behavior.valid.json exists
tests/test_unknown_external_perturbation_semantic_behavior.py exists
config/rtg_declared_tasks.json declares unknown_external_perturbation_semantic_behavior_tests
python tests/test_unknown_external_perturbation_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task unknown_external_perturbation_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
