# RTG Config Task Path Hotfix

## Purpose

This hotfix changes the registry task path back to the canonical RTG fixture smoke test.

The failed run attempted:

```text
tests/test_fixture_smoke.py
```

The correct canonical test is:

```text
tests/test_rtg_fixtures.py
```

## File Replaced

```text
config/rtg_declared_tasks.json
```

## Exact Correction

```json
{
  "name": "fixture_smoke_tests",
  "command": ["python", "tests/test_rtg_fixtures.py"]
}
```

## What This Does Not Change

```text
No workflow change.
No dispatcher change.
No test shim added.
No test files replaced.
```

## Verification

After upload, run:

```bash
python scripts/rtg_dispatcher.py --task fixture_smoke_tests
python scripts/rtg_dispatcher.py --task all
```

Expected output includes:

```text
RTG fixture smoke tests passed.
RTG repo dispatcher completed.
```
