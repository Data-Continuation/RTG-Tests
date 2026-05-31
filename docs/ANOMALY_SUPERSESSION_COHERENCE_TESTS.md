# RTG Anomaly Supersession Coherence Tests

## Purpose

This document defines a provisional executable RTG **cross-layer coherence** test for **anomaly supersession coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence
Layer: anomaly supersession coherence
Dispatcher: repo-local only
Canonical fixture smoke task: tests/test_rtg_fixtures.py
```

## Done State

This layer is done when:

```text
fixtures/anomaly-supersession-coherence.valid.json exists
tests/test_anomaly_supersession_coherence.py exists
config/rtg_declared_tasks.json declares anomaly_supersession_coherence_tests
python tests/test_anomaly_supersession_coherence.py passes
python scripts/rtg_dispatcher.py --task anomaly_supersession_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks that behavior from multiple earlier RTG layers remains coherent when combined.

## Non-Claim

This test does not prove final RTG mathematics.

It creates one provisional executable cross-layer constraint that can be revised as the formalism matures.
