# RTG Supersession Receipt Strength Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **supersession receipt strength semantic behavior**.

## Mechanism Group

```text
supersession
```

## Done State

```text
fixtures/supersession-receipt-strength-semantic-behavior.valid.json exists
tests/test_supersession_receipt_strength_semantic_behavior.py exists
config/rtg_declared_tasks.json declares supersession_receipt_strength_semantic_behavior_tests
python tests/test_supersession_receipt_strength_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task supersession_receipt_strength_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
