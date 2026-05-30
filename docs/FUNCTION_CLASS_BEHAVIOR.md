# RTG Function-Class Behavior

## Purpose

This document defines the first executable behavior layer for Relative Transition Geometry function classes.

The goal is to move beyond labels.

A function class should describe how a transition cell behaves under observation, admissibility pressure, risk resistance, stabilization, emission, and coupling.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: function-class behavior
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/function-classes.valid.json exists
tests/test_function_classes.py exists
config/rtg_declared_tasks.json declares function_class_behavior_tests
python tests/test_function_classes.py passes
python scripts/rtg_dispatcher.py --task function_class_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Provisional Function Classes

RTG currently recognizes these provisional function classes:

```text
bounded
slow_growth
steep_growth
singular
dampening
amplifying
bridging
barrier
resonant
```

## Behavior Profile Fields

Each function-class profile defines:

```text
class_name
description
pressure_growth
observation_effect
coupling_effect
stabilization_difficulty
emission_constraint
zeno_sensitivity
expected_behavior
```

## Allowed Scale

The first test uses a simple `0..1` scale.

```text
0.0 = minimal / absent
1.0 = maximal / dominant
```

`coupling_effect` may use `-1..1` because coupling can reduce, preserve, or amplify propagation.

## Behavioral Expectations

### bounded

A bounded class should keep pressure and Zeno sensitivity below runaway levels.

```text
pressure_growth <= 0.50
zeno_sensitivity <= 0.50
```

### slow_growth

A slow-growth class should accumulate pressure gradually.

```text
pressure_growth > bounded.pressure_growth
pressure_growth < steep_growth.pressure_growth
```

### steep_growth

A steep-growth class should rise sharply, but remain below singular behavior.

```text
pressure_growth > slow_growth.pressure_growth
pressure_growth < singular.pressure_growth
```

### singular

A singular class should have the highest pressure growth and high Zeno sensitivity.

```text
pressure_growth == max(all pressure_growth values)
zeno_sensitivity >= 0.80
```

### dampening

A dampening class should reduce propagation.

```text
coupling_effect < 0
```

### amplifying

An amplifying class should increase propagation.

```text
coupling_effect > 0
```

### bridging

A bridging class should have positive coupling and comparatively lower emission constraint than barrier.

```text
coupling_effect > 0
emission_constraint < barrier.emission_constraint
```

### barrier

A barrier class should strongly constrain emission.

```text
emission_constraint >= 0.80
coupling_effect <= 0
```

### resonant

A resonant class should support positive coupling while preserving moderate-to-high Zeno sensitivity.

```text
coupling_effect > 0
zeno_sensitivity >= 0.50
```

## Non-Claim

These profiles do not define final RTG mathematics.

They are provisional behavior contracts that make function classes testable.

## Why This Matters

Before this layer, `function_class` was a label.

After this layer, `function_class` begins to carry executable meaning.

That moves RTG from fixture structure into early behavior validation.
