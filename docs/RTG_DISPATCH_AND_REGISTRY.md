# RTG Dispatch and Registry

## Dispatcher Model

The repo uses a repo-local dispatcher.

The dispatcher reads:

```text
config/rtg_declared_tasks.json
```

and runs only declared tasks.

## Registry Rule

Every executable test task must be declared in:

```text
config/rtg_declared_tasks.json
```

A task declaration includes:

```json
{
  "name": "example_task",
  "description": "Validate example behavior.",
  "enabled": true,
  "command": ["python", "tests/test_example.py"]
}
```

## Unknown Task Rule

Unknown task names must be rejected.

This is intentional.

The dispatcher is not a free-form command runner.

## Canonical Fixture Task

```json
{
  "name": "fixture_smoke_tests",
  "command": ["python", "tests/test_rtg_fixtures.py"]
}
```

## Running All Tasks

```bash
python scripts/rtg_dispatcher.py --task all
```

## Running One Task

```bash
python scripts/rtg_dispatcher.py --task observer_identity_coupling_tests
```
