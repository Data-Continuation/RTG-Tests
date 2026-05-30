# RTG Coupling Model

## Assumption

Transition cells are not isolated.

A cell's state may affect other cells through translated coupling.

## Coupling Definition

A coupling edge describes how one cell's observed state influences another cell.

Provisional coupling parameters:

```text
source_cell
target_cell
relation_type
translation_weight
pressure_effect
confidence_effect
darkness_effect
emission_effect
notes
```

## Relation Types

Provisional relation types:

```text
shared_evidence
shared_authority
shared_policy
shared_risk
shared_observer_limit
shared_replay_path
dependency
analogy
resonance
barrier
```

## Translation Weight

`translation_weight` describes how much the source cell's posture translates into the target cell's local geometry.

A source cell may be important in its own region but only partially relevant to another cell.

```text
0.0 = no influence
1.0 = full local translation
```

## Coupling Effects

Effects may be positive, negative, or neutral.

```text
pressure_effect
    raises or lowers admissibility pressure

confidence_effect
    raises or lowers confidence

darkness_effect
    increases or decreases unobserved remainder

emission_effect
    increases or decreases emission readiness
```

## Core Principle

> Color tells us what has been observed. Function tells us how the cell behaves. Coupling tells us how that behavior alters the rest of the table.
