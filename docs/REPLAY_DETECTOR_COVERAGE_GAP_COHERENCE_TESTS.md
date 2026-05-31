# RTG Replay Detector Coverage Gap Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **replay detector coverage gap coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence
Layer: replay detector coverage gap coherence
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/replay-detector-coverage-gap-coherence.valid.json exists
tests/test_replay_detector_coverage_gap_coherence.py exists
config/rtg_declared_tasks.json declares replay_detector_coverage_gap_coherence_tests
python tests/test_replay_detector_coverage_gap_coherence.py passes
python scripts/rtg_dispatcher.py --task replay_detector_coverage_gap_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks cross-layer coherence among identity/authority, replay/receipt, lineage/export, risk, confidence, and finality gating.

## Non-Claim

This test does not prove final RTG mathematics.

It adds one provisional executable constraint that can be revised as the formalism matures.
