# RTG Math-Solver Adapter Layer

Generated: `2026-06-01T17:44:49Z`

## Purpose

The bridge exports individual RTG solver cases.

The adapter groups exported cases into a workflow-ready solver-run manifest for:

```text
GCAT-BCAT-Engine/workflows/math-solver
```

## Adapter Flow

```text
RTG fixtures
→ scripts/export_rtg_solver_cases.py
→ build/solver-cases/*.json
→ scripts/build_rtg_solver_run_manifest.py
→ build/solver-runs/rtg_solver_run_manifest.json
→ GCAT-BCAT-Engine/workflows/math-solver
→ solver result artifacts
→ RTG formal posture record
```

## Expected Solver Outputs

```text
build/solver-results/solver_results.json
build/solver-results/solver_summary.json
build/solver-results/rtg_formal_posture.json
```

## Done State

```text
python tests/test_rtg_math_solver_adapter.py passes
python scripts/build_rtg_solver_run_manifest.py writes a run manifest
config/rtg_declared_tasks.json declares rtg_math_solver_adapter_tests
python scripts/rtg_dispatcher.py --task rtg_math_solver_adapter_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Non-Claim

This adapter does not solve RTG.

It creates the stable solver-run contract that allows a downstream solver workflow to consume RTG solver cases.
