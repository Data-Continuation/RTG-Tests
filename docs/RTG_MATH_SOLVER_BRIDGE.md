# RTG Math-Solver Bridge

Generated: `2026-06-01T17:28:26Z`

## Purpose

This bridge converts RTG semantic fixture evidence into solver-ready cases for:

```text
GCAT-BCAT-Engine/workflows/math-solver
```

## Bridge Flow

```text
RTG semantic fixture
→ solver case export
→ formal variables
→ constraints
→ expected solver posture
→ math-solver workflow
→ solver result
→ RTG formal posture record
```

## Solver Postures

```text
satisfiable
contradictory
underconstrained
overconstrained
equivalent_to_prior_case
requires_new_axiom_or_operator
```

## Done State

```text
python tests/test_rtg_solver_case_export.py passes
python scripts/export_rtg_solver_cases.py exports solver cases
config/rtg_declared_tasks.json declares rtg_solver_case_export_tests
python scripts/rtg_dispatcher.py --task rtg_solver_case_export_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Non-Claim

This bridge does not solve RTG by itself. It creates the interface that allows RTG fixtures to become solver inputs.
