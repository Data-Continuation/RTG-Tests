# RTG Formalism Posture

## Maturity

RTG is currently:

```text
draft
speculative
provisional
executable
testable
not proof-complete
```

## What The Tests Mean

The tests do not prove that RTG is final.

They prove that specific RTG behavioral claims have been converted into machine-checkable constraints.

That is the important transition:

```text
conceptual claim
→ fixture
→ executable classifier
→ expected governance state
→ green/failed result
```

## What The Tests Do Not Mean

The tests do not mean:

```text
all transition classes are known
all observer classes are complete
all detector compatibility rules are final
all governance outputs are final
all mathematics is complete
```

## Formalism Boundary

The repo should preserve the distinction between:

```text
false_transition
unknown_unknown
```

A false transition is a bad or invalid transition claim.

An unknown unknown is a model limitation or hidden condition.

They require different governance outcomes.
