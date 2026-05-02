# v17.5 Runbook

Authoring status: authored

## Purpose

This runbook restores the v17.5 SLO lesson to its safe local-only state and
explains what to do when the reliability plan fails validation.

## Primary Checks

Run:

```bash
python3 examples/validate_service_agent_slo_plan.py
python3 examples/simulate_slo_error_budget.py
```

The safe state is:

- `slo_runtime_started` is `false`.
- `metrics_backend_started` is `false`.
- `alerting_runtime_started` is `false`.
- `dashboard_runtime_started` is `false`.
- `agent_runtime_started` is `false`.
- `provider_call_made` is `false`.
- all runtime limits are `0`.
- all SLO names use the `aois-p-` prefix.
- agent quality, safety, and human review gates are enabled.

## Recovery Steps

1. Restore all runtime flags to `false`.
2. Restore service SLOs for `aois-p-api` and
   `aois-p-incident-stream-consumer`.
3. Restore the agent SLO for `aois-p-incident-agent`.
4. Restore the required SLIs: availability, latency, freshness,
   agent success, agent quality, and agent safety.
5. Restore burn-rate alert policy.
6. Restore error-budget policy.
7. Restore dashboard policy.
8. Restore all runtime limits to `0`.
9. Rerun the validator and simulator.

If a live monitoring service was started outside this lesson, confirm it is not
part of the primary AOIS workload before stopping it. This curriculum must not
interfere with the primary project.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17.5 Lab](04-lab.md)
- Next: [v17.5 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
