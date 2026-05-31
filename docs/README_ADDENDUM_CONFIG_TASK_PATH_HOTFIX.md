# RTG Config Task Path Hotfix Addendum

## Install

Upload every file in this bundle to its exact path.

## Files

```text
config/rtg_declared_tasks.json
docs/CONFIG_TASK_PATH_HOTFIX.md
bundle_manifest.json
```

## Purpose

Restore the `fixture_smoke_tests` command to:

```text
python tests/test_rtg_fixtures.py
```

This is the clean registry-only fix for the failed dispatcher run.
