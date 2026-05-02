# v19 Runbook

Authoring status: authored

## Purpose

This runbook restores the v19 chaos engineering lesson to its safe local-only
state and explains how to correct validation failures.

## Primary Checks

Run:

```bash
python3 examples/validate_chaos_engineering_plan.py
python3 examples/simulate_chaos_game_day.py
```

The safe state is:

- `chaos_runtime_started` is `false`.
- `fault_injection_executed` is `false`.
- `load_test_started` is `false`.
- `network_fault_started` is `false`.
- `cpu_stress_started` is `false`.
- `memory_stress_started` is `false`.
- `pod_delete_executed` is `false`.
- `agent_runtime_started` is `false`.
- `provider_call_made` is `false`.
- all runtime and fault limits are `0`.
- all experiments have `approved_for_live_execution=false`.

## Recovery Steps

1. Restore all runtime and fault flags to `false`.
2. Restore principles: steady state, hypothesis, blast radius, abort condition,
   rollback, observer, communication, and primary AOIS protection.
3. Restore the three `aois-p` experiments.
4. Restore each experiment field: target, failure mode, hypothesis, steady
   state, blast radius, abort condition, rollback, SLO guardrail, and agent
   guardrail.
5. Restore game-day policy.
6. Restore safety controls.
7. Restore all limits to `0`.
8. Rerun the validator and simulator.

If any real stress, load, network, Kubernetes, or provider action was started
outside this lesson, stop and confirm it is not part of the primary AOIS
workload before changing it. This curriculum must not interfere with the
primary project.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19 Lab](lab.md)
- Next: [v19 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
