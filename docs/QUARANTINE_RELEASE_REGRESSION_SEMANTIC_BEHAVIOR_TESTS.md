# RTG Quarantine Release Regression Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **quarantine release regression semantic behavior**.

## Mechanism Group

```text
quarantine
```

## Done State

```text
fixtures/quarantine-release-regression-semantic-behavior.valid.json exists
tests/test_quarantine_release_regression_semantic_behavior.py exists
config/rtg_declared_tasks.json declares quarantine_release_regression_semantic_behavior_tests
python tests/test_quarantine_release_regression_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task quarantine_release_regression_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
