# RTG Formal Claim Gate Layer

Generated: `2026-06-02T02:16:26Z`

## Purpose

This layer prevents RTG from claiming formal or mathematical progress unless the formal posture registry satisfies explicit evidence thresholds.

## Gated Solver Evidence Chain

```text
RTG fixture
→ solver case
→ solver-run manifest
→ math-solver result
→ RTG formal posture record
→ RTG formal posture registry
→ RTG formal claim gate
```

## Gate Decisions

```text
allow_formal_claim
defer_claim
block_claim
```

## Default Thresholds

```text
minimum_record_count = 1
minimum_total_case_count = 1
required_ready_for_formal_claim_count = 1
maximum_formally_inconsistent_count = 0
maximum_blocked_count = 0
```

## Done State

```text
python tests/test_rtg_formal_claim_gate.py passes
python scripts/gate_rtg_formal_claim.py writes rtg_formal_claim_gate_decision.json
config/rtg_declared_tasks.json declares rtg_formal_claim_gate_tests
python scripts/rtg_dispatcher.py --task rtg_formal_claim_gate_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```
