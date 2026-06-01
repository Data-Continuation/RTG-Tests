# RTG Purpose Convergence Recoverability Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **purpose convergence recoverability semantic behavior**.

## Mechanism Group

```text
purpose
```

## Done State

```text
fixtures/purpose-convergence-recoverability-semantic-behavior.valid.json exists
tests/test_purpose_convergence_recoverability_semantic_behavior.py exists
config/rtg_declared_tasks.json declares purpose_convergence_recoverability_semantic_behavior_tests
python tests/test_purpose_convergence_recoverability_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task purpose_convergence_recoverability_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
