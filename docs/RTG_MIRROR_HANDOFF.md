# RTG Mirror Handoff

**Repository:** `Data-Continuation/RTG-Tests`  
**Formalism:** Relational / Relative Transition Geometry (RTG)  
**Updated:** 2026-07-27  
**Status:** Active formalization and executable proof-harness expansion

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

## Immediate Build Tasks

1. Add canonical schemas for candidate-transition fields, significance classes, transition constellations, reachable-state frontiers, and geometry deformation.
2. Add fixtures for active, supporting, latent, and discardable transition classes.
3. Add tests showing that low-immediate-significance transitions can become significant after contextual deformation.
4. Add micro-node allocation tests driven by topology, concurrency, uncertainty, coupling, and authority regimes.
5. Add transition-block formation and dissolution tests based on relational density and closure conditions.
6. Add decision-preserving compression tests for the insignificant-state substrate.
7. Add multi-trajectory simulations and deterministic receipts.
8. Integrate with `Admissible-Existence/TT` as the local discrete execution and admissibility surface.
9. Mirror public-facing definitions and status into `StegVerse-Labs/Site` after executable validation.

## Remaining Modules / Destinations

- `Data-Continuation/RTG-Tests`: schemas, fixtures, validators, simulations, receipts, workflows.
- `Admissible-Existence/AE`: canonical admissible-existence interpretation of RTG state fields.
- `Admissible-Existence/ae-validation-factory`: validation profiles and cross-formalism cases.
- `Admissible-Existence/TT`: transition-table resolution interface for bounded local decisions.
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
