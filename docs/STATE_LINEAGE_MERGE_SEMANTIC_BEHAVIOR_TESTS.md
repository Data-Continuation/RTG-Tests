# RTG State Lineage Merge Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **state lineage merge semantic behavior**.

## Mechanism Group

```text
state
```

## Done State

```text
fixtures/state-lineage-merge-semantic-behavior.valid.json exists
tests/test_state_lineage_merge_semantic_behavior.py exists
config/rtg_declared_tasks.json declares state_lineage_merge_semantic_behavior_tests
python tests/test_state_lineage_merge_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task state_lineage_merge_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
