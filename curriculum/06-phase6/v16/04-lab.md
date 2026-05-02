# v16 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_unified_telemetry_plan.py examples/simulate_unified_telemetry.py
python3 examples/validate_unified_telemetry_plan.py
python3 examples/simulate_unified_telemetry.py
```

## Ops Lab

Answer:

1. Did a collector start?
2. Did Prometheus, Loki, or Tempo start?
3. Which trace ID appears in traces, metrics, and logs?
4. Which metric proves no provider call happened?

Answer key:

1. no
2. no
3. `trace-v16-local-sim`
4. `aois_provider_call_count=0`

## Break Lab

Use a scratch copy only.

Break 1: set `tempo_started` to `true`.

Expected result: validation fails because no trace backend is approved.

Break 2: remove `trace_id` from correlation fields.

Expected result: validation fails because signals cannot be joined reliably.

Break 3: remove `secret_redaction_required`.

Expected result: validation fails because logs must not leak secrets.

## Explanation Lab

Explain:

1. Why logs alone are insufficient.
2. Why every signal needs correlation fields.
3. Why high-cardinality metrics can damage observability systems.
4. Why sampling policy is required.
5. Why telemetry backends are not started in this lesson.

## Defense Lab

Defend this decision:

AOIS should not run live telemetry services until instrumentation design, sampling, cardinality budget, retention, redaction tests, dashboards, alerts, storage budget, rollback, and primary AOIS separation exist.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v16 - Unified Telemetry Without Runtime](03-notes.md)
- Next: [v16 Runbook](05-runbook.md)
<!-- AOIS-NAV-END -->
