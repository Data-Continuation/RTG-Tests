# RTG Solver Result Ingestion Layer

Generated: `2026-06-01T20:21:01Z`

## Purpose

This layer closes the first RTG math-solver loop.

```text
RTG fixtures
→ solver cases
→ solver-run manifest
→ GCAT-BCAT-Engine/workflows/math-solver
→ solver_results.json
→ rtg_formal_posture.json
→ admissibility / formal posture evidence
```

## Formal Postures

```text
formally_consistent
formally_inconsistent
underconstrained
mixed_or_requires_review
blocked
```

## Case-Level Mapping

```text
satisfiable → admissible
contradictory → blocked
underconstrained → deferred
overconstrained → review
equivalent_to_prior_case → admissible_equivalent
requires_new_axiom_or_operator → requires_formal_extension
```

## Done State

```text
python tests/test_rtg_solver_result_ingestion.py passes
python scripts/ingest_rtg_solver_results.py writes rtg_formal_posture.json
config/rtg_declared_tasks.json declares rtg_solver_result_ingestion_tests
python scripts/rtg_dispatcher.py --task rtg_solver_result_ingestion_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```
