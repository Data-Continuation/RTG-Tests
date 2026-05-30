# RTG Coupling Translation Tests

## Purpose

This document defines the first executable coupling translation layer for Relative Transition Geometry.

The goal is to test how one transition cell changes another transition cell through translated influence.

Before this layer, coupling existed as descriptive fixture data.

After this layer, coupling begins to carry executable behavior.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: coupling translation
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/coupling-translation.valid.json exists
tests/test_coupling_translation.py exists
config/rtg_declared_tasks.json declares coupling_translation_tests
python tests/test_coupling_translation.py passes
python scripts/rtg_dispatcher.py --task coupling_translation_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Model

A coupling edge translates influence from a source cell into a target cell.

```text
translated_effect = translation_weight × raw_effect
```

The target cell then receives bounded updates:

```text
target.pressure  += translated_pressure_effect
target.confidence += translated_confidence_effect
target.darkness += translated_darkness_effect
target.emission += translated_emission_effect
```

All updated target posture fields remain bounded within `0..1`.

## Fixture Shape

The fixture contains:

```text
source_cells
target_cells
couplings
expected_targets_after_translation
```

Each coupling includes:

```text
source_cell
target_cell
relation_type
translation_weight
pressure_effect
confidence_effect
darkness_effect
emission_effect
```

## Tested Behaviors

### 1. Required cells exist

Every coupling must reference known source and target cells.

### 2. Translation weights are bounded

```text
0 <= translation_weight <= 1
```

### 3. Coupling effects are signed bounded values

```text
-1 <= effect <= 1
```

### 4. Translated effects are computed

```text
translated = effect × translation_weight
```

### 5. Target states are clamped

Post-translation fields cannot leave the `0..1` interval.

### 6. Barrier behavior can reduce emission

A barrier relation may lower target emission readiness and raise pressure.

### 7. Shared evidence can reduce darkness

A shared-evidence relation may reduce target darkness and raise confidence.

## Non-Claim

These tests do not prove final RTG coupling mathematics.

They only establish a provisional executable rule for translated cell-to-cell influence.

## Why This Matters

This is the first layer where the transition table behaves like a coupled field rather than isolated cells.

A cell can now affect another cell in a machine-checkable way.
