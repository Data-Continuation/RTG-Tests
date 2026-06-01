# RTG Semantic Claim Scope Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **semantic claim scope semantic behavior**.

## Mechanism Group

```text
semantic
```

## Done State

```text
fixtures/semantic-claim-scope-semantic-behavior.valid.json exists
tests/test_semantic_claim_scope_semantic_behavior.py exists
config/rtg_declared_tasks.json declares semantic_claim_scope_semantic_behavior_tests
python tests/test_semantic_claim_scope_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task semantic_claim_scope_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
