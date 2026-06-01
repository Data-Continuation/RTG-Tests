# RTG Authority Split Quorum Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **authority split quorum semantic behavior**.

## Mechanism Group

```text
authority
```

## Done State

```text
fixtures/authority-split-quorum-semantic-behavior.valid.json exists
tests/test_authority_split_quorum_semantic_behavior.py exists
config/rtg_declared_tasks.json declares authority_split_quorum_semantic_behavior_tests
python tests/test_authority_split_quorum_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task authority_split_quorum_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
