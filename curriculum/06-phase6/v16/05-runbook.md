# v16 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v16` telemetry plan to safe no-runtime state.

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_unified_telemetry_plan.py examples/simulate_unified_telemetry.py
python3 examples/validate_unified_telemetry_plan.py
python3 examples/simulate_unified_telemetry.py
```

Required:

- validator `status=pass`
- simulator `status=pass`
- no telemetry runtime
- no collector
- no metrics/logs/traces backends
- namespace is `aois-p`

## Recovery Steps

If validation fails:

1. Read `missing`.
2. Restore runtime/backend flags to `false`.
3. Restore `aois-p` component names.
4. Restore traces, metrics, logs, and correlation requirements.
5. Restore sampling, cardinality, and retention controls.
6. Restore live checks.
7. Rerun validation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v16 Lab](04-lab.md)
- Next: [v16 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
