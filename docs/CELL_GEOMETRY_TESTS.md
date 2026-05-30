# RTG Cell Geometry Tests

## Purpose

This document defines the first substantive test layer for `Data-Continuation/RTG-Tests`.

The goal is not to prove Relative Transition Geometry.

The goal is to begin testing whether a transition cell can be represented as a coherent local geometry with bounded posture values and basic relationships among observability, darkness, stabilization, and emission readiness.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative
Test status: provisional smoke layer
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/cell-geometry.valid.json exists
tests/test_cell_geometry.py exists
config/rtg_declared_tasks.json declares cell_geometry_smoke_tests
python tests/test_cell_geometry.py passes
python scripts/rtg_dispatcher.py --task all passes
```

## Tested Invariants

The first cell-geometry tests validate these provisional invariants.

### 1. Required field presence

A geometry fixture must include:

```text
cell_id
maturity
shell_role
function_class
governance_posture
observation
darkness
evidence_density
confidence
admissibility_pressure
risk_resistance
stabilization
emission_readiness
```

### 2. Unit interval posture values

The following fields must remain within `0..1`:

```text
observation
darkness
evidence_density
confidence
admissibility_pressure
risk_resistance
stabilization
emission_readiness
```

### 3. Darkness complement tolerance

Darkness is provisionally modeled as the unobserved or underclassified remainder.

The first test allows tolerance rather than exact equality:

```text
darkness ≈ 1 - observation
```

This is intentionally loose because future RTG definitions may include hidden-context darkness, coupling-inherited darkness, or unresolved replay darkness.

### 4. Emission requires stabilization

A cell should not be more ready to emit than it is stabilized.

```text
emission_readiness <= stabilization
```

This preserves the black-hole / white-hole transition intuition:

```text
compressed possibility
→ stabilization
→ governed emission
```

### 5. Confidence cannot exceed evidence plus observation support

Confidence should not outrun the available observed/evidence support.

The provisional ceiling is:

```text
confidence <= average(observation, evidence_density) + tolerance
```

This prevents a cell from claiming strong confidence without enough governed observation or evidence density.

### 6. Pressure-resistance balance is recorded

The test computes a provisional balance value:

```text
pressure_balance = admissibility_pressure - risk_resistance
```

This value may be negative, neutral, or positive.

The test does not yet enforce a maturity rule on pressure balance. It only requires the fixture to be numerically coherent.

## Non-Claim

These tests do not establish final RTG mathematics.

They only create a disciplined starting point for checking that cell-state examples are not arbitrary.

## Future Additions

Likely next layers:

```text
function-class behavior tests
coupling translation tests
shell-role expectation tests
Zeno-prone transition tests
dark-cell color emergence tests
stabilization-emission threshold tests
Site visualization parameter tests
```
