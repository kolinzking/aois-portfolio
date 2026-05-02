# v16.5 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_agent_incident_tracing_plan.py examples/simulate_agent_incident_trace.py
python3 examples/validate_agent_incident_tracing_plan.py
python3 examples/simulate_agent_incident_trace.py
```

## Ops Lab

Answer from the simulator:

1. How many incident steps are emitted?
2. Which step is the root?
3. Which step performs classification?
4. Which step proves provider execution remained disabled?
5. How many tool calls happened?

Answer key:

1. `6`
2. `incident.ingest`
3. `incident.classify`
4. `incident.route_decision`
5. `0`

## Break Lab

Use a scratch copy only.

Break 1: set `tool_calls_executed` to `true`.

Expected result: validation fails because this lesson executes no tools.

Break 2: remove `agent_run_id_required`.

Expected result: validation fails because future agent steps need a shared run ID.

Break 3: set `max_provider_calls_for_lesson` to `1`.

Expected result: validation fails because provider calls remain disallowed.

## Explanation Lab

Explain:

1. Why final response logs are insufficient.
2. Why parent-child step relationships matter.
3. Why each step needs a decision reason.
4. Why summaries must be redacted.
5. Why tool call IDs are required when tools are used.

## Defense Lab

Defend this decision:

AOIS should not enable live agent tracing until it has step taxonomy, tool-call trace policy, redaction tests, cardinality budget, sampling policy, incident timeline dashboard, trace storage budget, rollback, and primary AOIS separation.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v16.5 - Agent And Incident Tracing Without Runtime](notes.md)
- Next: [v16.5 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
