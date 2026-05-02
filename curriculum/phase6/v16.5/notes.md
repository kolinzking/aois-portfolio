# v16.5 - Agent And Incident Tracing Without Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: tracing plan and simulation only, no agent runtime, no tool calls, no provider calls, no collector, no trace backend

## What This Builds

This version builds an agent and incident tracing plan:

- `telemetry/aois-p/agent-incident-tracing.plan.json`
- `examples/validate_agent_incident_tracing_plan.py`
- `examples/simulate_agent_incident_trace.py`

It teaches:

- incident traces
- step traces
- parent-child step relationships
- agent-run placeholders
- tool-call trace policy
- incident timelines
- step metrics
- why multi-step behavior needs more than request logs

## Why This Exists

`v16` connected traces, metrics, and logs for one request.

AOIS now needs deeper traceability for multi-step behavior.

Incident and agent-style workflows involve decisions over time:

- ingest signal
- inspect security
- classify incident
- choose route
- recommend action
- emit response

Without step-level traces, operators cannot explain where a decision came from or which step failed.

## AOIS Connection

The AOIS path is now:

`unified telemetry -> incident trace -> agent trace -> streaming and SLOs`

`v16.5` does not run an agent. It prepares the tracing model needed before future agent runtime work.

## Learning Goals

By the end of this version you should be able to:

- explain an incident trace
- explain a step trace
- explain parent-child step relationships
- explain why agent runs need IDs
- explain when tool call IDs are required
- explain why input/output summaries must be redacted
- validate an incident tracing plan locally
- run a local multi-step trace simulation

## Prerequisites

You should have completed:

- `v16` unified telemetry

Required checks:

```bash
python3 -m py_compile examples/validate_agent_incident_tracing_plan.py examples/simulate_agent_incident_trace.py
python3 examples/validate_agent_incident_tracing_plan.py
python3 examples/simulate_agent_incident_trace.py
```

## Core Concepts

## Incident Trace

An incident trace is the timeline of work performed for one incident.

It connects intake, inspection, classification, routing, recommendation, and response.

## Step Trace

A step trace records one operation inside an incident trace.

Each step needs:

- step ID
- parent step ID
- status
- duration
- input summary
- output summary
- decision reason

## Agent Run ID

An agent run ID identifies one agent execution attempt.

In this lesson, it is a placeholder only. No agent runtime starts.

## Tool Call ID

A tool call ID is required when an agent uses a tool.

In this lesson, tool calls are not executed.

## Parent-Child Relationship

Parent-child relationships show how one step caused or followed another.

This turns a flat log list into a traceable timeline.

## Redacted Summaries

Input and output summaries must avoid secrets and sensitive content.

Trace data should help debugging without leaking protected data.

## Build

Inspect:

```bash
sed -n '1,280p' telemetry/aois-p/agent-incident-tracing.plan.json
sed -n '1,320p' examples/validate_agent_incident_tracing_plan.py
sed -n '1,280p' examples/simulate_agent_incident_trace.py
```

Compile:

```bash
python3 -m py_compile examples/validate_agent_incident_tracing_plan.py examples/simulate_agent_incident_trace.py
```

Validate:

```bash
python3 examples/validate_agent_incident_tracing_plan.py
```

Simulate:

```bash
python3 examples/simulate_agent_incident_trace.py
```

Expected validation:

```json
{
  "agent_runtime_started": false,
  "tool_calls_executed": false,
  "provider_call_made": false,
  "collector_started": false,
  "trace_backend_started": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the plan and simulator:

1. Which field proves no agent runtime started?
2. Which field proves no tool calls were executed?
3. Which field proves no provider call happened?
4. What is the root trace name?
5. Which step classifies the incident?
6. Which step records route decision?
7. Which ID links all steps to one placeholder agent run?
8. Which metric proves zero tool calls?

Answer key:

1. `agent_runtime_started=false`
2. `tool_calls_executed=false`
3. `provider_call_made=false`
4. `aois.incident_trace`
5. `incident.classify`
6. `incident.route_decision`
7. `agent_run_id`
8. `aois_agent_tool_calls_total=0`

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Start Agent Runtime Too Early

Set:

```json
"agent_runtime_started": true
```

Expected risk:

- a tracing lesson can be mistaken for permission to execute agent behavior

### Option B - Remove Parent Step IDs

Remove `parent_step_id` from required fields.

Expected risk:

- steps become a flat list and the incident timeline loses causality

### Option C - Remove Decision Reason

Set:

```json
"decision_reason_required": false
```

Expected risk:

- future operators can see what happened but not why

## Testing

The version passes when:

1. both scripts compile
2. validator returns `status=pass`
3. simulator returns `status=pass`
4. agent runtime remains false
5. tool calls remain false
6. provider calls remain false
7. collector and backend remain false
8. required steps are present
9. parent-child, duration, status, summaries, redaction, and decision reasons remain required

## Common Mistakes

- logging final output but not intermediate decisions
- missing parent-child step relationships
- recording raw sensitive input in traces
- tracing tool calls without tool call IDs
- treating agent run ID as optional
- starting live tracing backends before storage budget exists

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_agent_incident_tracing_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore runtime flags to `false`
- restore required step names
- restore required trace fields
- restore correlation policy
- restore step controls
- restore observability controls
- restore limits to zero
- restore required live checks

## Benchmark

Measure:

- validator compile result
- validator status
- simulator status
- step count
- tool call count
- provider call status
- collector/backend status
- repo disk footprint
- memory snapshot

## Architecture Defense

Why trace steps instead of only requests?

Because multi-step behavior can fail between request start and response finish.

Why require decision reasons?

Because incident response needs to explain why AOIS chose a route or recommendation.

Why keep agent runtime disabled?

Because this version teaches trace shape before executing future agents.

## 4-Layer Tool Drill

Tool: incident trace

1. Plain English
It shows the timeline of work for one incident.

2. System Role
It lets AOIS explain multi-step incident handling.

3. Minimal Technical Definition
It is a correlated sequence of step records connected by trace, incident, request, and parent-step identifiers.

4. Hands-on Proof
The simulator emits a six-step incident trace without starting an agent runtime.

## 4-Level System Explanation Drill

1. Simple English
AOIS traces incident steps without running an agent.

2. Practical Explanation
I can inspect each step, parent relationship, duration, status, input/output summary, and decision reason.

3. Technical Explanation
`v16.5` adds an incident tracing plan, validator, and local multi-step trace simulator.

4. Engineer-Level Explanation
AOIS now separates agent/incident trace design from agent execution, requiring step taxonomy, tool-call trace policy, redaction, cardinality budget, sampling, incident timeline dashboard, storage budget, rollback, and primary-project separation before live tracing is enabled.

## Failure Story

Representative failure:

- Symptom: AOIS recommends a memory investigation, but operators cannot tell whether that came from classification, routing, or a future agent step
- Root cause: only final response logs were recorded
- Fix: add incident step traces with decision reasons and parent-child relationships
- Prevention: validate the `v16.5` trace plan before adding agent runtime behavior
- What this taught me: final answers are not enough for operations

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v16.5` solve in AOIS?
2. What is an incident trace?
3. What is a step trace?
4. Why is parent step ID required?
5. Why is agent run ID required?
6. When is tool call ID required?
7. Why are decision reasons required?
8. Why must summaries be redacted?
9. Why is agent runtime disabled?
10. Explain incident trace using the 4-layer tool rule.
11. Explain `v16.5` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v16.5` solve in AOIS?

It makes multi-step incident and agent-style behavior inspectable before agent runtime exists.

2. What is an incident trace?

A timeline of work performed for one incident.

3. What is a step trace?

One timed operation inside an incident trace.

4. Why is parent step ID required?

It preserves causality between steps.

5. Why is agent run ID required?

It groups steps that belong to the same agent-style execution attempt.

6. When is tool call ID required?

When an agent or workflow executes a tool call.

7. Why are decision reasons required?

They explain why AOIS chose a route, classification, or recommendation.

8. Why must summaries be redacted?

Trace data must be useful without leaking secrets or sensitive content.

9. Why is agent runtime disabled?

This lesson designs trace shape only; live agent behavior needs separate governance.

10. Explain incident trace using the 4-layer tool rule.

- Plain English: it shows the timeline of one incident.
- System Role: it explains multi-step incident handling.
- Minimal Technical Definition: it is correlated step records linked by trace, incident, request, and parent-step IDs.
- Hands-on Proof: the simulator emits a six-step trace without agent runtime.

11. Explain `v16.5` using the 4-level system explanation rule.

- Simple English: AOIS traces incident steps without running an agent.
- Practical explanation: I can inspect steps, reasons, timings, and parent relationships.
- Technical explanation: `v16.5` adds a trace plan, validator, and simulator.
- Engineer-level explanation: AOIS gates live agent tracing behind step taxonomy, tool-call tracing, redaction, cardinality, sampling, timeline dashboards, storage budget, rollback, and primary separation.

## Connection Forward

`v16.5` makes multi-step behavior traceable.

`v17` moves to event streaming, where incident and telemetry events can be produced, consumed, replayed, and inspected over time.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v16.5 Introduction](introduction.md)
- Next: [v16.5 Lab](lab.md)
<!-- AOIS-NAV-END -->
