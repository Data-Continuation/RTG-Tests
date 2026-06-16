# RTG-001 Next Instruction Selection

## Purpose

This layer chooses the next governed instruction after RTG records a state update from ingested artifact evidence.

It starts from:

```text
rtg_state_update_recorded
```

and selects one of:

```text
route_to_review
route_to_replay
route_to_quarantine
route_to_solver_iteration
```

## Current Deterministic Rule

For RTG-001 first-pass / fixture-compatible evidence, the selected route is:

```text
route_to_review
```

Reason:

```text
The evidence may preserve claim boundary and cost receipt, but final correctness and autonomous theorem-proof claims remain blocked until human or formal review.
```

## Inputs

```text
status/rtg_001_state_update.json
```

## Output

```text
instructions/rtg_001/rtg_001_next_instruction.json
```

## Claim Boundary

Allowed after this layer:

```text
next_instruction_selected
route_to_review
```

Still blocked:

```text
autonomous_theorem_proving_claimed
final_correctness_claimed
```
