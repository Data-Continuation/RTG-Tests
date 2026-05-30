# RTG Shell-Role Expectation Tests

## Purpose

This document defines the first executable shell-role expectation layer for Relative Transition Geometry.

The goal is to make `s`, `p`, `d`, and `f` roles behave as provisional dynamic classes instead of only visual or descriptive labels.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: shell-role expectations
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/shell-roles.valid.json exists
tests/test_shell_roles.py exists
config/rtg_declared_tasks.json declares shell_role_expectation_tests
python tests/test_shell_roles.py passes
python scripts/rtg_dispatcher.py --task shell_role_expectation_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Shell Roles

RTG currently recognizes four provisional shell roles:

```text
s
p
d
f
```

These are inspired by the dynamic roles of s, p, d, and f orbital shells, but they are not chemical claims.

They are transition-governance role classes.

## Role Expectations

### s role

The `s` role is the foundational stabilizer.

Expected behavior:

```text
high repeatability
high stabilization bias
low coupling reach
low latent complexity
low ambiguity tolerance
```

### p role

The `p` role is the directional translator.

Expected behavior:

```text
moderate stabilization
higher directional coupling
medium ambiguity tolerance
orientation-sensitive translation
```

### d role

The `d` role is the coordination mediator.

Expected behavior:

```text
higher authority complexity
higher coupling reach
higher dispute or quarantine relevance
moderate-to-high stabilization demand
```

### f role

The `f` role is the deep complexity cell.

Expected behavior:

```text
high latent complexity
high observability burden
high stabilization demand
long-range coupling potential
slower emission readiness
```

## Tested Fields

Each shell-role profile defines:

```text
role
description
stabilization_bias
coupling_reach
authority_complexity
latent_complexity
observability_burden
emission_latency
ambiguity_tolerance
expected_behavior
```

All numeric fields are bounded within `0..1`.

## Provisional Cross-Role Invariants

The first shell-role tests validate:

```text
s.latent_complexity < p.latent_complexity < d.latent_complexity < f.latent_complexity

s.coupling_reach < p.coupling_reach
p.coupling_reach <= d.coupling_reach
f.observability_burden is highest
f.emission_latency is highest
s.stabilization_bias is high
d.authority_complexity > p.authority_complexity
```

## Non-Claim

These tests do not prove final RTG shell mathematics.

They create a provisional executable role contract for shell-like transition behavior.

## Why This Matters

Before this layer:

```text
shell_role described a cell
```

After this layer:

```text
shell_role constrains what kind of behavior a cell is expected to carry
```

This gives the Site a stronger basis for presenting cell depth and character.
