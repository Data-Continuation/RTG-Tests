# RTG Confidence Regrade Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **confidence regrade semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/confidence-regrade-semantic-behavior.valid.json exists
tests/test_confidence_regrade_semantic_behavior.py exists
config/rtg_declared_tasks.json declares confidence_regrade_semantic_behavior_tests
python tests/test_confidence_regrade_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task confidence_regrade_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Confidence regrade behavior changes confidence based on corroboration, contradiction, detector quality, and source drift.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
