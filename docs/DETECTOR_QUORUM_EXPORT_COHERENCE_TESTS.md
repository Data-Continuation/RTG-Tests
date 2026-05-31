# RTG Detector Quorum Export Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence task for **detector quorum export coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence next-31
Layer: detector quorum export coherence
Dispatcher: repo-local only
```

## Done State

```text
fixtures/detector-quorum-export-coherence.valid.json exists
tests/test_detector_quorum_export_coherence.py exists
config/rtg_declared_tasks.json declares detector_quorum_export_coherence_tests
python tests/test_detector_quorum_export_coherence.py passes
python scripts/rtg_dispatcher.py --task detector_quorum_export_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This task verifies that authority, lineage, replay, risk, and a task-specific secondary condition remain coherent as a combined transition packet.

## Non-Claim

This task does not prove final RTG mathematics. It adds one provisional executable coherence constraint that can be revised as the formalism matures.
