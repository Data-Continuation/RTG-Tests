# RTG Source Target Lineage Fork Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **source target lineage fork coherence**.

## Done State

```text
fixtures/source-target-lineage-fork-coherence.valid.json exists
tests/test_source_target_lineage_fork_coherence.py exists
config/rtg_declared_tasks.json declares source_target_lineage_fork_coherence_tests
python tests/test_source_target_lineage_fork_coherence.py passes
python scripts/rtg_dispatcher.py --task source_target_lineage_fork_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
