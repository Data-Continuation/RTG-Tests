# RTG Identity Detector Authority Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence task for **identity detector authority coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence next-31
Layer: identity detector authority coherence
Dispatcher: repo-local only
```

## Done State

```text
fixtures/identity-detector-authority-coherence.valid.json exists
tests/test_identity_detector_authority_coherence.py exists
config/rtg_declared_tasks.json declares identity_detector_authority_coherence_tests
python tests/test_identity_detector_authority_coherence.py passes
python scripts/rtg_dispatcher.py --task identity_detector_authority_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This task verifies that authority, lineage, replay, risk, and a task-specific secondary condition remain coherent as a combined transition packet.

## Non-Claim

This task does not prove final RTG mathematics. It adds one provisional executable coherence constraint that can be revised as the formalism matures.
