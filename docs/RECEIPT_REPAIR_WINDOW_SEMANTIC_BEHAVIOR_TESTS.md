# RTG Receipt Repair Window Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **receipt repair window semantic behavior**.

## Mechanism Group

```text
receipt
```

## Done State

```text
fixtures/receipt-repair-window-semantic-behavior.valid.json exists
tests/test_receipt_repair_window_semantic_behavior.py exists
config/rtg_declared_tasks.json declares receipt_repair_window_semantic_behavior_tests
python tests/test_receipt_repair_window_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task receipt_repair_window_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
