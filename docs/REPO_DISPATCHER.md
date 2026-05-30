# RTG Repo Dispatcher

## Purpose

This document describes the repo-local dispatcher workflow for `Data-Continuation/RTG-Tests`.

The dispatcher is intended to become the stable entry point for all declared RTG test tasks in this repository.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Scope: repo-local only
Secrets: none
Write access: none
External repo calls: none
Declared task registry: config/rtg_declared_tasks.json
Workflow: .github/workflows/rtg-repo-dispatcher.yml
```

Note: the workflow path above is shown with its leading dot because it is a canonical GitHub path. In ordinary display contexts where leading-dot paths are problematic, display it as `github/workflows/rtg-repo-dispatcher.yml` and note that the leading dot was removed for display only.

## Done State

The dispatcher is considered installed when:

```text
.github/workflows/rtg-repo-dispatcher.yml exists
config/rtg_declared_tasks.json exists
scripts/rtg_dispatcher.py exists
scripts/verify_rtg_dispatcher.py exists
python scripts/verify_rtg_dispatcher.py passes
python scripts/rtg_dispatcher.py --task all passes
```

## Declared Task Model

All executable tasks must be declared in:

```text
config/rtg_declared_tasks.json
```

A task has:

```text
name
description
enabled
command
```

The dispatcher rejects undeclared tasks.

## Current Declared Tasks

```text
fixture_smoke_tests
    runs provisional RTG fixture validation

dispatcher_self_check
    verifies dispatcher contract behavior
```

## Running Locally

List declared tasks:

```bash
python scripts/rtg_dispatcher.py --list
```

Dry-run all enabled tasks:

```bash
python scripts/rtg_dispatcher.py --task all --dry-run
```

Run all enabled tasks:

```bash
python scripts/rtg_dispatcher.py --task all
```

Run one declared task:

```bash
python scripts/rtg_dispatcher.py --task fixture_smoke_tests
```

Verify the dispatcher contract:

```bash
python scripts/verify_rtg_dispatcher.py
```

## GitHub Actions

The workflow supports:

```text
manual workflow_dispatch
push to main affecting dispatcher/test files
pull_request to main affecting dispatcher/test files
```

Manual dispatch accepts:

```text
task
dry_run
```

Use `task=all` to run every enabled declared task.

## Security and Stability Posture

The dispatcher is intentionally conservative.

```text
permissions: contents: read
no repository writes
no external repo calls
no secrets required
unknown tasks rejected
disabled tasks rejected
declared command executables restricted to python/python3
```

## Adding a New Task

Add a new object to `config/rtg_declared_tasks.json`.

Example:

```json
{
  "name": "new_task_name",
  "description": "Describe what this task validates.",
  "enabled": true,
  "command": ["python", "tests/new_test_file.py"]
}
```

Then verify:

```bash
python scripts/verify_rtg_dispatcher.py
python scripts/rtg_dispatcher.py --task all
```

## Non-Claim

This dispatcher does not prove RTG. It only creates a stable repo-local mechanism for running declared RTG tests as the formalism matures.
