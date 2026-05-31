# RTG Unknown Unknown Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **unknown unknown semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/unknown-unknown-semantic-behavior.valid.json exists
tests/test_unknown_unknown_semantic_behavior.py exists
config/rtg_declared_tasks.json declares unknown_unknown_semantic_behavior_tests
python tests/test_unknown_unknown_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task unknown_unknown_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Unknown-unknown behavior does not reject a claim as false; it lowers posture, widens review, or preserves anomaly.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
