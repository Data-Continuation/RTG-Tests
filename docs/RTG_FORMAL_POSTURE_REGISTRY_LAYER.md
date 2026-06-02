# RTG Formal Posture Registry Layer

Generated: `2026-06-01T20:31:11Z`

## Purpose

This layer persists RTG formal posture records generated from math-solver outputs.

The solver loop now becomes indexable:

```text
RTG fixture
→ solver case
→ solver-run manifest
→ math-solver result
→ RTG formal posture record
→ RTG formal posture registry
```

## Registry Function

The registry tracks solver-ingested formal posture evidence by:

```text
solver_run_id
formal_posture
case_count
source_path
source_sha256
source_solver_results
receipt
```

## Formal Postures Indexed

```text
formally_consistent
formally_inconsistent
underconstrained
mixed_or_requires_review
blocked
```

## Summary Counts

The registry summarizes:

```text
record_count
total_case_count
formal_posture_counts
ready_for_formal_claim_count
review_required_count
```

## Done State

```text
python tests/test_rtg_formal_posture_registry.py passes
python scripts/register_rtg_formal_postures.py writes rtg_formal_posture_registry.json
config/rtg_declared_tasks.json declares rtg_formal_posture_registry_tests
python scripts/rtg_dispatcher.py --task rtg_formal_posture_registry_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Non-Claim

This registry does not prove RTG mathematical completeness.

It persists and summarizes solver-ingested formal posture evidence so formal progress can be tracked.
