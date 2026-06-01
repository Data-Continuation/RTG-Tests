# RTG Dark Evidence Saturation Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **dark evidence saturation semantic behavior**.

## Mechanism Group

```text
dark
```

## Done State

```text
fixtures/dark-evidence-saturation-semantic-behavior.valid.json exists
tests/test_dark_evidence_saturation_semantic_behavior.py exists
config/rtg_declared_tasks.json declares dark_evidence_saturation_semantic_behavior_tests
python tests/test_dark_evidence_saturation_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task dark_evidence_saturation_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
