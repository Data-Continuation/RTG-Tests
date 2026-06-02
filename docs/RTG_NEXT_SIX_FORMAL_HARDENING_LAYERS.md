# RTG Next Six Formal Hardening Layers

Generated: `2026-06-02T04:00:28Z`

## Purpose

This bundle adds the next six formal hardening layers after axiom/operator/invariant construction.

```text
counterexample search
contradiction classification
equivalence-class reduction
axiom independence check
proof-obligation registry
coverage geometry scoring
```

## Non-Claim

These layers harden candidate formalism evidence. They do not claim final mathematical completeness.

## Done State

```text
python tests/test_rtg_counterexample_search.py passes
python tests/test_rtg_contradiction_classification.py passes
python tests/test_rtg_equivalence_reduction.py passes
python tests/test_rtg_axiom_independence.py passes
python tests/test_rtg_proof_obligation_registry.py passes
python tests/test_rtg_coverage_geometry_scoring.py passes
config/rtg_declared_tasks.json declares all six new tasks
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```
