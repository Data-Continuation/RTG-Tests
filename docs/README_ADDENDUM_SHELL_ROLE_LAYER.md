# RTG Shell-Role Layer Addendum

## Purpose

This addendum summarizes the shell-role expectation layer added after the green coupling translation baseline.

## Files Added or Replaced

```text
config/rtg_declared_tasks.json
docs/SHELL_ROLE_EXPECTATION_TESTS.md
fixtures/shell-roles.valid.json
tests/test_shell_roles.py
```

## Dispatcher Task Added

```text
shell_role_expectation_tests
```

The task runs:

```bash
python tests/test_shell_roles.py
```

## Verification

Run:

```bash
python tests/test_shell_roles.py
python scripts/rtg_dispatcher.py --task shell_role_expectation_tests
python scripts/rtg_dispatcher.py --task all
```

Expected outputs include:

```text
RTG shell-role expectation tests passed.
RTG repo dispatcher completed.
```

## What Changed

Before this layer:

```text
shell_role described the cell
```

After this layer:

```text
shell_role constrains expected transition behavior
```

## Roles Covered

```text
s
p
d
f
```

## Non-Claim

This layer does not prove RTG.

It creates the first machine-checkable expectation profile for shell-like RTG transition roles.
