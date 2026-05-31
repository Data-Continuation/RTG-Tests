# RTG Supersession Quorum Replay Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **supersession quorum replay coherence**.

## Done State

```text
fixtures/supersession-quorum-replay-coherence.valid.json exists
tests/test_supersession_quorum_replay_coherence.py exists
config/rtg_declared_tasks.json declares supersession_quorum_replay_coherence_tests
python tests/test_supersession_quorum_replay_coherence.py passes
python scripts/rtg_dispatcher.py --task supersession_quorum_replay_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
