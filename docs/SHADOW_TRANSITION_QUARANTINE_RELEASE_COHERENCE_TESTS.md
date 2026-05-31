# RTG Shadow Transition Quarantine Release Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **shadow transition quarantine release coherence**.

## Done State

```text
fixtures/shadow-transition-quarantine-release-coherence.valid.json exists
tests/test_shadow_transition_quarantine_release_coherence.py exists
config/rtg_declared_tasks.json declares shadow_transition_quarantine_release_coherence_tests
python tests/test_shadow_transition_quarantine_release_coherence.py passes
python scripts/rtg_dispatcher.py --task shadow_transition_quarantine_release_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
