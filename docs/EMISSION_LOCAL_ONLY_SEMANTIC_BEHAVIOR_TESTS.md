# RTG Emission Local Only Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **emission local only semantic behavior**.

## Mechanism Group

```text
emission
```

## Done State

```text
fixtures/emission-local-only-semantic-behavior.valid.json exists
tests/test_emission_local_only_semantic_behavior.py exists
config/rtg_declared_tasks.json declares emission_local_only_semantic_behavior_tests
python tests/test_emission_local_only_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task emission_local_only_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
