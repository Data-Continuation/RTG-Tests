# RTG Observer-Window Tests

## Purpose

This document defines the first executable observer-window layer for Relative Transition Geometry.

The goal is to test what an observer can see, miss, classify, defer, or emit based on the window through which the transition is observed.

This connects RTG directly to inference-window behavior.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: observer-window behavior
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/observer-windows.valid.json exists
tests/test_observer_windows.py exists
config/rtg_declared_tasks.json declares observer_window_tests
python tests/test_observer_windows.py passes
python scripts/rtg_dispatcher.py --task observer_window_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Principle

> Observation does not reveal reality equally. It reveals what the observer-window permits the system to see, classify, and emit.

## Provisional Model

Each observer-window case defines:

```text
case_id
window_scope
window_duration
window_resolution
observer_authority
evidence_access
confidence
target_visibility
expected_observation_state
```

The provisional observation states are:

```text
missed
seen_unclassified
classified_deferred
classified_emittable
overclaimed
```

## Window Capacity

This layer computes provisional window capacity as:

```text
window_capacity =
    average(
        window_scope,
        window_duration,
        window_resolution,
        observer_authority,
        evidence_access,
        confidence
    )
```

Target visibility remains a separate field because a transition may be visible in the environment but still unavailable to the observer.

## Behavior Rules

### Missed

The observer-window lacks enough capacity or visibility.

```text
target_visibility < visibility_min
or window_capacity < missed_capacity_max
```

### Seen but unclassified

The observer can see the target, but not enough structure exists to classify it.

```text
target_visibility >= visibility_min
window_capacity is low-to-moderate
```

### Classified but deferred

The observer can classify the target, but lacks enough authority, evidence, or confidence to emit it.

```text
window_capacity >= classification_min
window_capacity < emission_min
```

### Classified and emittable

The observer has enough visibility, evidence, confidence, and authority to emit a governed classification.

```text
window_capacity >= emission_min
observer_authority >= authority_min_for_emission
```

### Overclaimed

The observer claims emission while authority, confidence, or evidence is insufficient.

```text
claimed_emission == true
classified_emittable == false
```

## Non-Claim

These tests do not prove final RTG observer mathematics.

They establish the first machine-checkable rule for observer-window limits.

## Why This Matters

This layer protects RTG from pretending that every observation has equal authority.

It also supports the transition-table idea that dark regions may remain dark because the observer-window is too narrow, too brief, too coarse, too weakly authorized, or too poorly evidenced.
