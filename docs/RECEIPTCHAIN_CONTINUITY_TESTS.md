# RTG Receipt-chain continuity Tests

## Purpose

This document defines a provisional executable RTG test layer for **receipt-chain continuity**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: receipt-chain continuity
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/receipt-chain-continuity.valid.json exists
tests/test_receipt_chain_continuity.py exists
config/rtg_declared_tasks.json declares receipt_chain_continuity_tests
python tests/test_receipt_chain_continuity.py passes
python scripts/rtg_dispatcher.py --task receipt_chain_continuity_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **receipt-chain continuity** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
