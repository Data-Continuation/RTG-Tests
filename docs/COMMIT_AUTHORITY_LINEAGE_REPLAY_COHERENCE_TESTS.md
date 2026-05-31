# RTG Commit Authority Lineage Replay Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence task for **commit authority lineage replay coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence next-31
Layer: commit authority lineage replay coherence
Dispatcher: repo-local only
```

## Done State

```text
fixtures/commit-authority-lineage-replay-coherence.valid.json exists
tests/test_commit_authority_lineage_replay_coherence.py exists
config/rtg_declared_tasks.json declares commit_authority_lineage_replay_coherence_tests
python tests/test_commit_authority_lineage_replay_coherence.py passes
python scripts/rtg_dispatcher.py --task commit_authority_lineage_replay_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This task verifies that authority, lineage, replay, risk, and a task-specific secondary condition remain coherent as a combined transition packet.

## Non-Claim

This task does not prove final RTG mathematics. It adds one provisional executable coherence constraint that can be revised as the formalism matures.
