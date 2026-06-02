# RTG Math-Solver Wiring Bundle

Generated: `2026-06-02T04:26:11Z`

## Purpose

This bundle wires RTG to the actual math-solver workflow boundary.

The target workflow reference is:

```text
GCAT-BCAT-Engine/workflows/math-solver
```

## Added Layers

```text
actual math-solver dispatch packet
math-solver interface contract
math-solver execution status
solver result return
end-to-end solver loop
```

## Important Boundary

This bundle prepares RTG-side dispatch and return handling. It does not claim that the external GitHub workflow has actually executed inside this sandbox.

The governed condition is:

```text
do_not_mark_complete_until_solver_results_json_exists
```

## Done State

```text
python tests/test_rtg_actual_math_solver_dispatch.py passes
python tests/test_rtg_math_solver_interface_contract.py passes
python tests/test_rtg_math_solver_execution_status.py passes
python tests/test_rtg_solver_result_return.py passes
python tests/test_rtg_end_to_end_solver_loop.py passes
config/rtg_declared_tasks.json declares all five new tasks
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```
