# RTG Mirror Handoff

**Repository:** `Data-Continuation/RTG-Tests`  
**Formalism:** Relational / Relative Transition Geometry (RTG)  
**Updated:** 2026-07-27  
**Status:** Active executable proof-harness expansion on `rtg-multi-trajectory-executable`

## Current Source of Truth

This document is the current handoff and task source of truth for RTG work in this repository.

RTG models reality-facing AI traversal as a dynamically deforming relational transition field rather than a linear sequence of state changes. The repository already contains executable constraints for cell geometry, coupling, observer windows, authority, replay, lineage, confidence, quarantine, anomaly retention, supersession, and commit finality.

## Current Goal

Encode and test the multi-trajectory RTG model in which:

- many candidate transitions coexist over very small time scales;
- only a subset is immediately significant;
- apparently insignificant transitions remain as supporting, latent, or discardable substrate;
- significance depends on causal, temporal, authority, evidentiary, identity, risk, and future-reachability relations;
- transition blocks form around relational density rather than linear task order;
- micro-node demand depends on concurrency, uncertainty, coupling, and authority complexity;
- AI action deforms the future reachable-state geometry.

## Canonical Conceptual Addition

See `docs/MULTI_TRAJECTORY_RELATIONAL_TRANSITION_GEOMETRY.md`.

## Completed on Active Branch

1. Candidate-transition field JSON Schema.
2. Canonical fixture containing active, supporting, latent, and discardable transitions.
3. Reachable-state frontier and geometry-deformation representation.
4. Significance-threshold and latent-promotion tests.
5. Topology-driven micro-node demand test.
6. Transition-block relational-density operator.
7. Transition-block formation and dissolution tests.
8. Significant-state constellation activation operator and test.
9. Decision-preserving substrate-compression signature and tests.
10. Deterministic SHA-256 deformation receipt operator and replay test.
11. Governed extension registry for multi-trajectory tasks.
12. Dispatcher support for canonical plus namespaced extension registries.
13. Bounded RTG-to-Transition-Table request schema and fixture.
14. Contract test preventing RTG from pre-deciding TT admissibility or execution.
15. Deterministic chained JSONL receipt operator.
16. Receipt-chain replay, tamper, and ordering tests.
17. Baseline dispatcher workflow run 180 completed successfully before extension registration.

## Active Pull Request

- Draft PR #1: `Add executable multi-trajectory RTG field model`
- Branch: `rtg-multi-trajectory-executable`
- Formalism posture remains draft/provisional until the latest extended dispatcher run is green.

## Immediate Build Tasks

1. Verify all extension-registry tasks through the RTG Repo Dispatcher workflow.
2. Add an executable multi-step trajectory simulation using the operators.
3. Persist a canonical example JSONL receipt chain for that simulation.
4. Add negative cases for false constellation activation and destructive compression.
5. Add Transition Table result schema and bounded request/result correlation tests.
6. Integrate the contract into `Admissible-Existence/TT` as the local discrete execution and admissibility surface.
7. Add validation-factory profiles in `Admissible-Existence/ae-validation-factory`.
8. Mirror public-facing definitions and status into `StegVerse-Labs/Site` after executable validation.

## Remaining Modules / Destinations

- `Data-Continuation/RTG-Tests`: simulation, canonical JSONL artifact, negative fixtures, TT result adapter, workflow verification.
- `Admissible-Existence/AE`: canonical admissible-existence interpretation of RTG state fields.
- `Admissible-Existence/ae-validation-factory`: validation profiles and cross-formalism cases.
- `Admissible-Existence/TT`: transition-table request/result resolution interface for bounded local decisions.
- `StegVerse-Labs/Site`: public visualization and explanatory model.
- `GCAT-BCAT-Engine/Publisher`: publication packaging when formalism reaches release posture.
- `admissibility-wiki`, `stegguardian-wiki`: terminology and governance implications after validation.

## Maturity Rule

No RTG result may be described as mathematically complete or proven unless its formal definition, assumptions, fixtures, expected result, actual result, and admissibility rationale are all identified and independently reproducible.

## Release Condition

A release/tag candidate requires:

- canonical definitions and schemas;
- green deterministic tests;
- replayable receipts;
- documented non-claims;
- cross-repository integration verification;
- confirmed updates to Site, Publisher, admissibility-wiki, and stegguardian-wiki.
