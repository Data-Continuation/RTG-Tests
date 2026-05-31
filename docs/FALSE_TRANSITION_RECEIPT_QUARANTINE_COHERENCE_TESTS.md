# RTG False Transition Receipt Quarantine Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence task for **false transition receipt quarantine coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence next-31
Layer: false transition receipt quarantine coherence
Dispatcher: repo-local only
```

## Done State

```text
fixtures/false-transition-receipt-quarantine-coherence.valid.json exists
tests/test_false_transition_receipt_quarantine_coherence.py exists
config/rtg_declared_tasks.json declares false_transition_receipt_quarantine_coherence_tests
python tests/test_false_transition_receipt_quarantine_coherence.py passes
python scripts/rtg_dispatcher.py --task false_transition_receipt_quarantine_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This task verifies that authority, lineage, replay, risk, and a task-specific secondary condition remain coherent as a combined transition packet.

## Non-Claim

This task does not prove final RTG mathematics. It adds one provisional executable coherence constraint that can be revised as the formalism matures.
