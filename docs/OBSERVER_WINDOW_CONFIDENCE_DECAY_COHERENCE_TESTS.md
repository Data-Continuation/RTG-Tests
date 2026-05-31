# RTG Observer Window Confidence Decay Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **observer window confidence decay coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence
Layer: observer window confidence decay coherence
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/observer-window-confidence-decay-coherence.valid.json exists
tests/test_observer_window_confidence_decay_coherence.py exists
config/rtg_declared_tasks.json declares observer_window_confidence_decay_coherence_tests
python tests/test_observer_window_confidence_decay_coherence.py passes
python scripts/rtg_dispatcher.py --task observer_window_confidence_decay_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks cross-layer coherence among identity/authority, replay/receipt, lineage/export, risk, confidence, and finality gating.

## Non-Claim

This test does not prove final RTG mathematics.

It adds one provisional executable constraint that can be revised as the formalism matures.
