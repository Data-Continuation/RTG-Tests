# RTG Transition Packet Replay Surface Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **transition packet replay surface semantic behavior**.

## Mechanism Group

```text
transition
```

## Done State

```text
fixtures/transition-packet-replay-surface-semantic-behavior.valid.json exists
tests/test_transition_packet_replay_surface_semantic_behavior.py exists
config/rtg_declared_tasks.json declares transition_packet_replay_surface_semantic_behavior_tests
python tests/test_transition_packet_replay_surface_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task transition_packet_replay_surface_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
