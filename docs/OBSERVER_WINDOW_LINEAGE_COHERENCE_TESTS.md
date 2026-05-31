# RTG Observer Window Lineage Coherence Tests

## Purpose

This document defines a provisional executable RTG **cross-layer coherence** test for **observer window lineage coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence
Layer: observer window lineage coherence
Dispatcher: repo-local only
Canonical fixture smoke task: tests/test_rtg_fixtures.py
```

## Done State

This layer is done when:

```text
fixtures/observer-window-lineage-coherence.valid.json exists
tests/test_observer_window_lineage_coherence.py exists
config/rtg_declared_tasks.json declares observer_window_lineage_coherence_tests
python tests/test_observer_window_lineage_coherence.py passes
python scripts/rtg_dispatcher.py --task observer_window_lineage_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks that behavior from multiple earlier RTG layers remains coherent when combined.

## Non-Claim

This test does not prove final RTG mathematics.

It creates one provisional executable cross-layer constraint that can be revised as the formalism matures.
