# RTG Governance Model

## Governance Principle

RTG treats transition governance as layered constraint validation.

A transition must not be accepted merely because it is visible, forceful, repeated, or confidently asserted.

## Governance Outcomes

Current governance outcomes include:

```text
accept
reject
defer
quarantine
require_replay
mark_provisional
widen_observer_window
preserve_anomaly
release
supersede
block_export
accept_state_evidence
```

## Boundary Classes

RTG currently recognizes governance boundaries across:

```text
visibility
classification
admissibility
authority
replayability
receipt continuity
lineage integrity
risk pressure
quarantine state
export boundary
finality
```

## Consequence Boundary Rule

The higher the consequence of a transition, the more layers must remain coherent before emission or finality.

## Quarantine Rule

Quarantine is not failure by default.

Quarantine is a governed holding state for transitions that may be:

```text
invalid
dangerous
underclassified
overclaimed
receipt-conflicted
lineage-conflicted
risk-elevated
not yet replayable
```

## Provisional Rule

A provisional state is not the same as an accepted state.

A provisional state preserves context while preventing premature finality.
