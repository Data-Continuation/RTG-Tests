# RTG Coupling-replay consistency Tests

## Purpose

This document defines a provisional executable RTG test layer for **coupling-replay consistency**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: coupling-replay consistency
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/coupling-replay-consistency.valid.json exists
tests/test_coupling_replay_consistency.py exists
config/rtg_declared_tasks.json declares coupling_replay_consistency_tests
python tests/test_coupling_replay_consistency.py passes
python scripts/rtg_dispatcher.py --task coupling_replay_consistency_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **coupling-replay consistency** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
