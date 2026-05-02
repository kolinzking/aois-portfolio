# v16 - Unified Telemetry Without Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: telemetry plan and simulation only, no OpenTelemetry install, no collector, no Prometheus, no Loki, no Tempo, no persistent storage

## What This Builds

This version builds a unified telemetry plan:

- `telemetry/aois-p/unified-telemetry.plan.json`
- `examples/validate_unified_telemetry_plan.py`
- `examples/simulate_unified_telemetry.py`

It teaches:

- traces
- spans
- metrics
- structured logs
- trace/log/metric correlation
- sampling policy
- cardinality budget
- retention policy
- Prometheus, Loki, and Tempo roles
- why logs alone are not observability

## Why This Exists

AOIS is now large enough that behavior must be visible.

Infrastructure, inference, routing, security inspection, and future agents cannot be operated by reading isolated logs.

Unified telemetry gives AOIS a common way to ask:

- what happened?
- where did time go?
- what failed?
- which request caused it?
- which route/model/tool was involved?
- what should be alerted?

## AOIS Connection

The AOIS path is now:

`inference engineering -> unified telemetry -> incident and agent tracing -> streaming and reliability`

Phase 6 makes AOIS observable before adding more complex runtime behavior.

## Learning Goals

By the end of this version you should be able to:

- explain traces, spans, metrics, and logs
- explain correlation fields
- explain why trace IDs must appear in logs and metrics
- explain why cardinality budgets matter
- explain why sampling policy is required
- explain the roles of Prometheus, Loki, and Tempo at a high level
- validate a telemetry plan locally without starting telemetry services
- run a local telemetry simulation

## Prerequisites

You should have completed:

- Phase 1 reliability baseline
- Phase 3 infrastructure planning
- Phase 5 inference engineering

Required checks:

```bash
python3 -m py_compile examples/validate_unified_telemetry_plan.py examples/simulate_unified_telemetry.py
python3 examples/validate_unified_telemetry_plan.py
python3 examples/simulate_unified_telemetry.py
```

## Core Concepts

## Trace

A trace is the full path of one request or workflow.

It is made of spans.

## Span

A span is one timed operation inside a trace.

AOIS planned spans:

- `aois.request`
- `aois.security_inspect`
- `aois.route_decision`
- `aois.analysis`
- `aois.response`

## Metric

A metric is a numeric measurement over time.

Examples:

- request count
- request latency
- error count
- route selection count
- provider call count

## Structured Log

A structured log is machine-readable event text, usually JSON-shaped.

It should carry trace and request identifiers.

## Correlation

Correlation means traces, metrics, and logs share identifiers.

Without correlation, operators manually guess which log belongs to which request.

## Cardinality Budget

Cardinality is how many unique label combinations exist.

High-cardinality metrics can break monitoring systems and waste memory/storage.

## Sampling Policy

Sampling policy decides how much trace data is kept.

It balances visibility against storage and cost.

## Build

Inspect:

```bash
sed -n '1,280p' telemetry/aois-p/unified-telemetry.plan.json
sed -n '1,320p' examples/validate_unified_telemetry_plan.py
sed -n '1,260p' examples/simulate_unified_telemetry.py
```

Compile:

```bash
python3 -m py_compile examples/validate_unified_telemetry_plan.py examples/simulate_unified_telemetry.py
```

Validate:

```bash
python3 examples/validate_unified_telemetry_plan.py
```

Simulate:

```bash
python3 examples/simulate_unified_telemetry.py
```

Expected validation:

```json
{
  "telemetry_runtime_started": false,
  "collector_started": false,
  "prometheus_started": false,
  "loki_started": false,
  "tempo_started": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the plan and simulator:

1. Which field proves no telemetry runtime started?
2. Which field proves no collector started?
3. Which components represent metrics, logs, and traces backends?
4. Which fields correlate traces, metrics, and logs?
5. Which planned span is the root span?
6. Which controls prevent telemetry from becoming too expensive?

Answer key:

1. `telemetry_runtime_started=false`
2. `collector_started=false`
3. `aois-p-prometheus-placeholder`, `aois-p-loki-placeholder`, and `aois-p-tempo-placeholder`
4. `trace_id`, `span_id`, `request_id`, `incident_id`, and `route_id`
5. `aois.request`
6. sampling policy, cardinality budget, retention policy, and storage budget

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Start Collector Too Early

Set:

```json
"collector_started": true
```

Expected risk:

- a plan-only lesson may be mistaken for live telemetry deployment

### Option B - Remove Trace ID From Logs

Set:

```json
"trace_id_required": false
```

Expected risk:

- logs cannot be connected reliably to traces

### Option C - Remove Cardinality Budget

Set:

```json
"cardinality_budget_required": false
```

Expected risk:

- metrics labels may grow unbounded and damage storage/memory usage

## Testing

The version passes when:

1. both scripts compile
2. validator returns `status=pass`
3. simulator returns `status=pass`
4. no telemetry runtime starts
5. no collector starts
6. no telemetry backend starts
7. traces, metrics, logs, and correlation remain required
8. sampling, cardinality, retention, dashboard, and alert controls remain required

## Common Mistakes

- treating logs as enough
- missing trace IDs in logs
- adding high-cardinality metric labels
- collecting everything without sampling policy
- keeping telemetry forever without retention policy
- starting observability services before resource budget exists
- mixing `aois-p` telemetry with primary AOIS telemetry

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_unified_telemetry_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore runtime and backend flags to `false`
- restore `aois-p` names
- restore correlation fields
- restore trace spans
- restore metric and log requirements
- restore sampling, cardinality, and retention controls
- restore live checks

## Benchmark

Measure:

- validator compile result
- validator status
- simulator status
- number of spans
- number of metrics
- number of structured logs
- runtime/backend status
- repo disk footprint
- memory snapshot

## Architecture Defense

Why not start telemetry services now?

Because telemetry backends consume memory and storage. This lesson first defines the signal contract and resource controls.

Why require correlation?

Because disconnected logs, metrics, and traces make incident debugging slow and unreliable.

Why require cardinality budget?

Because high-cardinality telemetry can become its own outage.

## 4-Layer Tool Drill

Tool: trace

1. Plain English
It shows the path one request took through the system.

2. System Role
It connects operations across components and time.

3. Minimal Technical Definition
It is a tree or graph of spans sharing a trace identifier.

4. Hands-on Proof
The simulator emits one trace with root and child spans without starting a telemetry runtime.

## 4-Level System Explanation Drill

1. Simple English
AOIS plans traces, metrics, and logs without running telemetry services.

2. Practical Explanation
I can inspect the planned spans, metrics, logs, and correlation fields.

3. Technical Explanation
`v16` adds a unified telemetry plan, validator, and local signal simulator.

4. Engineer-Level Explanation
AOIS now separates telemetry design from telemetry deployment, requiring instrumentation design, sampling policy, cardinality budget, retention policy, secret redaction, dashboards, alerts, storage budget, rollback, and primary-project separation before live telemetry services run.

## Failure Story

Representative failure:

- Symptom: a route decision causes slow responses, but logs, metrics, and traces cannot be connected
- Root cause: logs omitted trace IDs and metrics used unrelated labels
- Fix: add shared correlation fields to traces, metrics, and logs
- Prevention: validate unified telemetry before runtime instrumentation
- What this taught me: observability starts with correlation design

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v16` solve in AOIS?
2. What is a trace?
3. What is a span?
4. What is a metric?
5. What is a structured log?
6. Why is correlation required?
7. Why is cardinality budget required?
8. Why is sampling policy required?
9. Why are telemetry services not started?
10. Explain trace using the 4-layer tool rule.
11. Explain `v16` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v16` solve in AOIS?

It defines how AOIS traces, metrics, and logs connect before telemetry services run.

2. What is a trace?

The path of one request or workflow through the system.

3. What is a span?

One timed operation inside a trace.

4. What is a metric?

A numeric measurement over time.

5. What is a structured log?

A machine-readable event record with fields like severity, message, and trace ID.

6. Why is correlation required?

It connects logs, metrics, and traces for the same request or incident.

7. Why is cardinality budget required?

It prevents unbounded metric label growth from damaging telemetry storage and memory.

8. Why is sampling policy required?

It balances trace visibility against storage and cost.

9. Why are telemetry services not started?

This lesson is plan and simulation only; live telemetry needs docs review and resource budget.

10. Explain trace using the 4-layer tool rule.

- Plain English: it shows where one request went.
- System Role: it connects operations across components.
- Minimal Technical Definition: it is spans sharing a trace identifier.
- Hands-on Proof: the simulator emits a trace with root and child spans.

11. Explain `v16` using the 4-level system explanation rule.

- Simple English: AOIS plans observability without running telemetry services.
- Practical explanation: I can inspect traces, metrics, logs, and correlation fields.
- Technical explanation: `v16` adds a telemetry plan, validator, and simulator.
- Engineer-level explanation: AOIS gates live telemetry behind instrumentation design, sampling, cardinality, retention, redaction, dashboards, alerts, storage budget, rollback, and primary-separation controls.

## Connection Forward

`v16` defines unified telemetry.

`v16.5` builds deeper incident and agent tracing on top of these correlation rules.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v16 Introduction](introduction.md)
- Next: [v16 Lab](lab.md)
<!-- AOIS-NAV-END -->
