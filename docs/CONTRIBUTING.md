# Contributing to RTG-Tests

## Ground Rules

RTG tests should be:

```text
small
explicit
fixture-backed
repo-local
dispatcher-declared
documented
provisional unless proven otherwise
```

## Adding a Test

Every new test layer should include:

```text
fixtures/<layer>.valid.json
tests/test_<layer>.py
docs/<LAYER>_TESTS.md
```

The task must be declared in:

```text
config/rtg_declared_tasks.json
```

## Test Shape

Each test should normally include:

```text
valid states
cases
classifier or validator
expected state
all-states-covered check
classification check
```

## Documentation Shape

Each doc should include:

```text
Purpose
Assumptions
Done State
Core Rule
Non-Claim
```

## Registry Safety

Do not turn the dispatcher into a general command executor.

Keep commands simple:

```json
["python", "tests/test_example.py"]
```

## Canonical Fixture Smoke Test

Preserve:

```text
fixture_smoke_tests → python tests/test_rtg_fixtures.py
```
