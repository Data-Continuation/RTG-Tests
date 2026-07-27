# RTG Mirror Handoff

**Repository:** `Data-Continuation/RTG-Tests`  
**Formalism:** Relational / Relative Transition Geometry (RTG)  
**Updated:** 2026-07-27  
**Status:** Verified executable proof-harness expansion on `rtg-multi-trajectory-executable`

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
17. Executable latent-to-active trajectory simulation.
18. Persisted canonical JSONL simulation receipt chain.
19. Transition Table result schema and correlated result fixture.
20. Result correlation tests for request identity, candidate identity, authority/evidence closure, and authorization consistency.
21. Negative cases for mismatched requests, unknown evidence, execution without commit, and contradictory DENY outcomes.
22. RTG Repo Dispatcher run 198 completed successfully on branch head `22b2b6885581b8c476387f4c51fc97da49120d67`.
23. Reciprocal adapter opened in `Admissible-Existence/TT` PR #1.
24. TT Admissible Resolution Validation run 3 and TT Validation run 204 completed successfully.

## Active Pull Requests

- `Data-Continuation/RTG-Tests` PR #1: `Add executable multi-trajectory RTG field model`
- `Admissible-Existence/TT` PR #1: `Add bounded RTG request/result adapter`

Both branches are verified and may move from draft into review posture. The formalism remains provisional; verification establishes executable consistency, not mathematical completeness.

## Immediate Build Tasks

1. Add cross-repository receipt verification using exported RTG request and TT result artifacts.
2. Add negative fixtures for false constellation activation and destructive substrate compression as durable files.
3. Add validation-factory profiles in `Admissible-Existence/ae-validation-factory`.
4. Add the AE interpretation connecting geometric minimum-node declarations to the Admissible Resolution Function.
5. Generate propagation bundle updates in TT.
6. Mirror public-facing definitions and verified status into `StegVerse-Labs/Site` and `StegVerse-Labs/admissibility-wiki`.
7. Evaluate release/tag posture after cross-repository verification and propagation are green.

## Remaining Modules / Destinations

- `Data-Continuation/RTG-Tests`: cross-repository receipt verification, durable negative fixtures, release snapshot.
- `Admissible-Existence/AE`: canonical admissible-existence interpretation of RTG state fields.
- `Admissible-Existence/ae-validation-factory`: validation profiles and cross-formalism cases.
- `Admissible-Existence/TT`: workflow registration, propagation bundle updates, cross-repository receipt verification.
- `StegVerse-Labs/Site`: public visualization and explanatory model.
- `GCAT-BCAT-Engine/Publisher`: publication packaging when formalism reaches release posture.
- `StegVerse-Labs/admissibility-wiki`, `stegguardian-wiki`: terminology and governance implications after validation.

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

The complete thread is ready for archiving; this handoff and the two active PRs contain the full state needed to continue.
