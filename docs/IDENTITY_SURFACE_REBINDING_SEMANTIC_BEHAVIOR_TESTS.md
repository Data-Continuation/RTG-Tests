# RTG Identity Surface Rebinding Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **identity surface rebinding semantic behavior**.

## Mechanism Group

```text
identity
```

## Done State

```text
fixtures/identity-surface-rebinding-semantic-behavior.valid.json exists
tests/test_identity_surface_rebinding_semantic_behavior.py exists
config/rtg_declared_tasks.json declares identity_surface_rebinding_semantic_behavior_tests
python tests/test_identity_surface_rebinding_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task identity_surface_rebinding_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
