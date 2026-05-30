# RTG-Tests

**Repository:** `Data-Continuation/RTG-Tests`  
**Formalism family:** Relative Transition Geometry  
**Status:** Draft / speculative / provisional  
**Generated:** 2026-05-29

## Purpose

`RTG-Tests` is the provisional test and proof harness for **Relative Transition Geometry**.

Relative Transition Geometry, or RTG, models StegVerse transition cells as local geometries of:

- observability;
- admissibility pressure;
- evidence density;
- confidence posture;
- stabilization behavior;
- emission readiness;
- darkness / unobserved remainder;
- cell-to-cell translated coupling;
- shell-like dynamic roles.

This repository is intentionally **not proof-complete**.

It exists to preserve the first executable structure for testing the emerging mathematics without claiming that the formalism is finished.

## Current Maturity

```text
Conceptual structure: identified
Canonical mathematics: incomplete
Test coverage: provisional
Proof claims: not yet
Operational posture: scaffold only
```

RTG should currently be treated as:

```text
DRAFT / SPECULATIVE
```

It may later advance toward:

```text
PROVISIONAL
→ TESTED
→ PROVEN
```

only after definitions, fixtures, and validation rules are mature enough to support those claims.

## Relationship to Other Repositories

Recommended structure:

```text
formalisms/relative-transition-geometry
    canonical definitions
    axioms
    terminology
    equations
    diagrams
    examples
    Site presentation model

Data-Continuation/RTG-Tests
    provisional tests
    fixtures
    validators
    smoke checks
    expected output examples
```

Existing Stage 1–34 work in the broader formalism test lineage remains separate. RTG begins a new formalism family and should not be silently treated as Stage 35 unless that is explicitly decided later.

## Core RTG Premise

A transition cell is not a static box.

A transition cell may have:

```text
position
color
darkness
pressure
curvature
confidence
stabilization
emission readiness
function behavior
coupling behavior
shell role
```

A cell becomes visually and formally meaningful as admissibility-at-commit observations accumulate.

## Key Principle

> A dark transition cell is not an absence of reality. It is an absence of governed observability.

## Test Scope

The first tests in this repository are intentionally minimal. They validate that early RTG fixtures are structurally coherent.

Initial test targets:

1. Cell-state fixture shape.
2. Coupling fixture shape.
3. Required posture fields.
4. Bounded numeric fields.
5. Valid function-class names.
6. Valid shell-role names.
7. Basic translated coupling references.

These tests do **not** prove RTG. They only confirm that provisional examples are machine-readable and internally consistent.

## Current Files

```text
README.md
docs/RTG_FORMALISM_POSTURE.md
docs/CELL_MODEL.md
docs/SHELL_ROLES.md
docs/COUPLING_MODEL.md
fixtures/cell-state.example.json
fixtures/coupling.example.json
tests/test_rtg_fixtures.py
```

## Running the Smoke Tests

From the repository root:

```bash
python tests/test_rtg_fixtures.py
```

Expected result:

```text
RTG fixture smoke tests passed.
```

## Integrity Rule

No RTG test should claim proof maturity unless it can identify:

```text
the formal definition being tested
the assumptions under which it holds
the fixture or transition case used
the expected result
the actual result
the reason the result is admissible
```

## Site Visualization Direction

The Site should eventually present each transition cell as a governed state object with visible depth and character.

Possible visual mappings:

```text
color      = governance posture
brightness = confidence / evidence density
opacity    = darkness / uncertainty
height     = admissibility pressure
pulse      = unresolved active transition
border     = quarantine / rejection / risk posture
glow       = emission readiness
edges      = coupling to other cells
motion     = stabilization or instability
```

This repository does not implement the Site presentation. It only provides early test fixtures that can later support that presentation.

## Non-Claim

This repository does not claim that RTG is complete, proven, or mathematically final.

It preserves a disciplined beginning.
