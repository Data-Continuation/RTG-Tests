# RTG Observer Window Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **observer window semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/observer-window-semantic-behavior.valid.json exists
tests/test_observer_window_semantic_behavior.py exists
config/rtg_declared_tasks.json declares observer_window_semantic_behavior_tests
python tests/test_observer_window_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task observer_window_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Observer-window behavior is governed by overlap among event time, observer aperture, detector latency, and minimum dwell time.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
