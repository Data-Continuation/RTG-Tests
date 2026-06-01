# RTG Finality Commit Lock Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **finality commit lock semantic behavior**.

## Mechanism Group

```text
finality
```

## Done State

```text
fixtures/finality-commit-lock-semantic-behavior.valid.json exists
tests/test_finality_commit_lock_semantic_behavior.py exists
config/rtg_declared_tasks.json declares finality_commit_lock_semantic_behavior_tests
python tests/test_finality_commit_lock_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task finality_commit_lock_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
