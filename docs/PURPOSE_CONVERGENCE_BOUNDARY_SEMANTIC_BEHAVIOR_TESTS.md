# RTG Purpose Convergence Boundary Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **purpose convergence boundary semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/purpose-convergence-boundary-semantic-behavior.valid.json exists
tests/test_purpose_convergence_boundary_semantic_behavior.py exists
config/rtg_declared_tasks.json declares purpose_convergence_boundary_semantic_behavior_tests
python tests/test_purpose_convergence_boundary_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task purpose_convergence_boundary_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Purpose-convergence behavior detects boundaries that prevent harm while defeating the state they were meant to support.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
