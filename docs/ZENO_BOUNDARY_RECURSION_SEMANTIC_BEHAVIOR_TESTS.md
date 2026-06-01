# RTG Zeno Boundary Recursion Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **zeno boundary recursion semantic behavior**.

## Mechanism Group

```text
zeno
```

## Done State

```text
fixtures/zeno-boundary-recursion-semantic-behavior.valid.json exists
tests/test_zeno_boundary_recursion_semantic_behavior.py exists
config/rtg_declared_tasks.json declares zeno_boundary_recursion_semantic_behavior_tests
python tests/test_zeno_boundary_recursion_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task zeno_boundary_recursion_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
