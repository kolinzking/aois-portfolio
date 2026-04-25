# v16.5 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v16.5` agent and incident tracing plan to safe no-runtime state.

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_agent_incident_tracing_plan.py examples/simulate_agent_incident_trace.py
python3 examples/validate_agent_incident_tracing_plan.py
python3 examples/simulate_agent_incident_trace.py
```

Required:

- validator `status=pass`
- simulator `status=pass`
- agent runtime is false
- tool calls are false
- provider call is false
- collector/backend are false
- namespace is `aois-p`

## Recovery Steps

If validation fails:

1. Read `missing`.
2. Restore runtime/execution flags to `false`.
3. Restore required step names.
4. Restore required trace fields.
5. Restore correlation policy.
6. Restore step controls.
7. Restore observability controls.
8. Restore limits to zero.
9. Restore live checks.
