# RTG Master Record Reconstruction Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **master record reconstruction semantic behavior**.

## Mechanism Group

```text
master
```

## Done State

```text
fixtures/master-record-reconstruction-semantic-behavior.valid.json exists
tests/test_master_record_reconstruction_semantic_behavior.py exists
config/rtg_declared_tasks.json declares master_record_reconstruction_semantic_behavior_tests
python tests/test_master_record_reconstruction_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task master_record_reconstruction_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
