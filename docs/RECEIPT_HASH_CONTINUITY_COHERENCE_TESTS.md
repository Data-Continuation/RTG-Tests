# RTG Receipt Hash Continuity Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence task for **receipt hash continuity coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence next-31
Layer: receipt hash continuity coherence
Dispatcher: repo-local only
```

## Done State

```text
fixtures/receipt-hash-continuity-coherence.valid.json exists
tests/test_receipt_hash_continuity_coherence.py exists
config/rtg_declared_tasks.json declares receipt_hash_continuity_coherence_tests
python tests/test_receipt_hash_continuity_coherence.py passes
python scripts/rtg_dispatcher.py --task receipt_hash_continuity_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This task verifies that authority, lineage, replay, risk, and a task-specific secondary condition remain coherent as a combined transition packet.

## Non-Claim

This task does not prove final RTG mathematics. It adds one provisional executable coherence constraint that can be revised as the formalism matures.
