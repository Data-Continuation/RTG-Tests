# RTG Multi Entity Boundary Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **multi entity boundary semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/multi-entity-boundary-semantic-behavior.valid.json exists
tests/test_multi_entity_boundary_semantic_behavior.py exists
config/rtg_declared_tasks.json declares multi_entity_boundary_semantic_behavior_tests
python tests/test_multi_entity_boundary_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task multi_entity_boundary_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Multi-entity boundary behavior evaluates coupled authority, interference, and recoverability among interacting entities.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
