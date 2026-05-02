# v18 - Incident Response Maturity Without Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: incident response plan and simulation only, no pager runtime, no ticketing runtime, no chatops runtime, no status page runtime, no agent runtime, no provider call

## What This Builds

This version builds an incident response plan:

- `incident-response/aois-p/incident-response.plan.json`
- `examples/validate_incident_response_plan.py`
- `examples/simulate_incident_response.py`

It teaches:

- severity levels
- incident roles
- incident lifecycle
- triage and declaration
- stabilization and mitigation
- communication cadence
- agent safety gates during incidents
- post-incident review
- action items with owners and due dates
- why incident response is a control system, not just a document

## Why This Exists

v17.5 gave AOIS SLOs and error budgets.

The next question is operational:

```text
When an SLO burns or an agent becomes unsafe, what does the operator do?
```

Without incident response maturity:

- alerts become noise
- severity is assigned inconsistently
- nobody clearly owns the incident
- communication becomes scattered
- root cause is claimed before evidence exists
- risky agent actions can continue during degraded trust
- the same failure repeats because no review creates durable fixes

Incident response turns reliability signals into coordinated action.

## AOIS Connection

The AOIS path is now:

`telemetry -> tracing -> event streaming -> SLOs -> incident response`

v18 treats agent incidents as first-class operational events. If the agent SLO is exhausted, AOIS must not blindly continue automation. It must stabilize, route risky actions to human review, preserve evidence, communicate clearly, and produce follow-up work.

This version does not start live pager, ticketing, chatops, or status page tooling. It teaches the response model first.

## Learning Goals

By the end of this version you should be able to:

- explain why incident response comes after SLOs
- define SEV1, SEV2, and SEV3 for AOIS
- explain incident commander, operations lead, communications lead, scribe, subject matter expert, and agent operator roles
- explain the incident lifecycle from detect to review
- distinguish mitigation from resolution
- write safe incident communications
- explain why root cause must wait for evidence
- explain how agent safety gates change during incidents
- validate an incident response plan locally
- simulate a local incident timeline without runtime services

## Prerequisites

You should have completed:

- `v16` unified telemetry
- `v16.5` agent and incident tracing
- `v17` event streaming
- `v17.5` service and agent SLOs

Required checks:

```bash
python3 -m py_compile examples/validate_incident_response_plan.py examples/simulate_incident_response.py
python3 examples/validate_incident_response_plan.py
python3 examples/simulate_incident_response.py
```

## Core Concepts

## Incident

An incident is an event that threatens user impact, system reliability, safety, or operational trust.

In AOIS, incidents can come from:

- API failure
- event lag
- SLO burn
- unsafe agent recommendation
- provider failure
- resource pressure
- primary project interference risk

An incident is not just "something broke." It is a coordinated response state.

## Severity

Severity defines urgency and coordination level.

The v18 plan uses:

- `SEV1`: critical user or primary-system impact
- `SEV2`: major degradation, SLO burn, or unsafe agent behavior
- `SEV3`: limited degradation or recoverable operational risk

Severity is not about blame. It is about response intensity.

## Incident Commander

The incident commander owns coordination.

They do not need to be the deepest technical expert. Their job is to keep the incident structured:

- confirm severity
- assign roles
- keep the timeline moving
- make escalation decisions
- prevent chaos
- decide when the incident is resolved

## Operations Lead

The operations lead drives technical mitigation.

They inspect signals, test hypotheses, apply safe mitigations, and coordinate with subject matter experts.

## Communications Lead

The communications lead writes clear updates.

Good incident communication explains:

- what is impacted
- who is affected
- what is being done
- when the next update will happen
- what is not yet known

Bad communication guesses root cause too early.

## Scribe

The scribe maintains the timeline.

The timeline is not bureaucracy. It is evidence. It helps with coordination during the incident and review after the incident.

## Agent Operator

The agent operator is responsible for AI-specific controls during an incident.

They decide whether to:

- freeze prompt changes
- freeze tool changes
- route recommendations to human review
- block destructive actions
- inspect quality gate failures
- preserve agent traces and outputs

## Lifecycle

The v18 lifecycle is:

1. Detect
2. Triage
3. Declare
4. Stabilize
5. Mitigate
6. Resolve
7. Review

Do not skip declaration. A declared incident creates ownership and cadence.

## Triage

Triage answers:

- What symptom is visible?
- What is the user or operator impact?
- Which SLO is affected?
- Is an agent acting unsafely?
- Is the primary AOIS project at risk?
- What severity fits the current evidence?

Triage is not root cause analysis. It is fast classification for response.

## Mitigation

Mitigation reduces impact.

Examples:

- route agent actions to human review
- disable a risky workflow
- roll back a recent change
- scale down a secondary workload
- pause a noisy consumer
- increase operator review before action

Mitigation can happen before root cause is fully known.

## Resolution

Resolution means the incident exit criteria are met.

Examples:

- the affected SLO returns inside acceptable bounds
- unsafe agent outputs are blocked
- user impact has stopped
- the rollback is stable
- the incident commander confirms no active mitigation gap remains

Resolution does not mean learning is complete.

## Post-Incident Review

Post-incident review turns failure into durable improvement.

It should include:

- timeline
- impact summary
- contributing factors
- what went well
- what went poorly
- action items
- owners
- due dates
- SLO impact
- agent behavior review

It should not be a blame document.

## Build

Inspect:

```bash
sed -n '1,320p' incident-response/aois-p/incident-response.plan.json
sed -n '1,340p' examples/validate_incident_response_plan.py
sed -n '1,260p' examples/simulate_incident_response.py
```

Compile:

```bash
python3 -m py_compile examples/validate_incident_response_plan.py examples/simulate_incident_response.py
```

Validate:

```bash
python3 examples/validate_incident_response_plan.py
```

Simulate:

```bash
python3 examples/simulate_incident_response.py
```

Expected validation:

```json
{
  "incident_runtime_started": false,
  "pager_runtime_started": false,
  "ticketing_runtime_started": false,
  "chatops_runtime_started": false,
  "status_page_runtime_started": false,
  "agent_runtime_started": false,
  "provider_call_made": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

Expected simulation:

- incident id is `incident-v18-local-sim`
- severity is `SEV2`
- trigger is agent error budget exhaustion
- risky recommendations are routed to human review
- prompt and tool changes are frozen
- post-incident review is required
- no runtime service is started

## Ops Lab

Answer from the plan and simulator:

1. What severity is used for major degradation, SLO burn, or unsafe agent behavior?
2. Who coordinates the incident?
3. Who owns communication?
4. Who preserves the incident timeline?
5. What lifecycle step comes after triage?
6. What action is taken when the incident agent budget is exhausted?
7. Which fields prove no pager or chatops runtime started?
8. Why is root cause not claimed before evidence?

Answer key:

1. `SEV2`
2. `incident_commander`
3. `communications_lead`
4. `scribe`
5. `declare`
6. Route destructive or low-confidence recommendations to human review.
7. `pager_runtime_started=false` and `chatops_runtime_started=false`
8. Premature root cause claims mislead operators and can cause the wrong mitigation.

## Break Lab

Use a scratch copy or reversible local edit only.

### Option A - Start Pager Runtime

Set:

```json
"pager_runtime_started": true
```

Expected validator result:

- `pager_runtime_started_must_be_false`

Risk:

- a curriculum lesson becomes a live paging deployment without routing approval.

### Option B - Remove Incident Commander

Remove:

```json
"incident_commander": "aois-p-incident-commander-placeholder"
```

Expected validator result:

- `role_must_use_aois_p_prefix:incident_commander`

Risk:

- nobody owns coordination.

### Option C - Disable Human Approval For Destructive Action

Set:

```json
"human_approval_for_destructive_action": false
```

Expected validator result:

- `missing_agent_control:human_approval_for_destructive_action`

Risk:

- degraded trust does not stop unsafe automation.

## Testing

Run:

```bash
python3 -m py_compile examples/validate_incident_response_plan.py examples/simulate_incident_response.py
python3 examples/validate_incident_response_plan.py
python3 examples/simulate_incident_response.py
```

Pass criteria:

- scripts compile
- validator status is `pass`
- simulator status is `pass`
- all runtime flags are false
- timeline includes detect, triage, declare, stabilize, mitigate, resolve, and review
- action items have owners and due dates

## Common Mistakes

Mistake 1: Treating incident response as only a runbook.

Correction: incident response is a live coordination system with roles, severity, timeline, communications, mitigation, and review.

Mistake 2: Waiting for root cause before mitigating.

Correction: mitigate impact first when safe. Root cause can come later.

Mistake 3: Letting the most technical person automatically command the incident.

Correction: the incident commander coordinates. The technical lead investigates.

Mistake 4: Ignoring agent-specific incident behavior.

Correction: during incidents, agent prompts, tool calls, and destructive actions need stricter gates.

Mistake 5: Ending the incident at resolution.

Correction: review and action items are part of the incident lifecycle.

## Troubleshooting

If validation fails:

1. Confirm every runtime flag is false.
2. Confirm namespace is `aois-p`.
3. Confirm severities include `SEV1`, `SEV2`, and `SEV3`.
4. Confirm every role uses an `aois-p-` placeholder.
5. Confirm lifecycle includes detect, triage, declare, stabilize, mitigate, resolve, and review.
6. Confirm communication policy prevents root cause claims before evidence.
7. Confirm agent incident controls require human approval and tool-call audit.
8. Confirm limits are zero.

If simulation fails:

1. Confirm the plan file exists.
2. Confirm required roles exist.
3. Confirm the simulator references the same role keys as the plan.

## Benchmark

Record:

- validator status
- simulator status
- runtime services started
- severity count
- role count
- lifecycle step count
- communication update count
- action item count
- repo size
- `.venv` size
- memory available

This benchmark proves incident response structure, not live pager throughput.

## Architecture Defense

Defend these choices:

1. v18 does not start pager, ticketing, chatops, or status page systems because policy and coordination can be learned without runtime cost.
2. Agent incidents are first-class because AI outputs can fail even when infrastructure is available.
3. Severity is required because not every incident deserves the same response intensity.
4. A single incident commander is required because shared ownership often becomes no ownership.
5. Communication cadence is required because silence creates confusion during incidents.
6. Post-incident review is required because unresolved learning becomes repeated failure.

## 4-Layer Tool Drill

Explain incident response through the 4-layer tool rule:

1. Human goal: reduce impact and restore trust during degraded operation.
2. Interface: severity policy, runbooks, incident channel, updates, review template.
3. Mechanism: roles, lifecycle, escalation, mitigation, communication cadence, action items.
4. Substrate: telemetry, traces, event streams, SLOs, logs, agent outputs, infrastructure state.

Answer key:

Incident response is not the pager tool. The pager is only an interface. The mechanism is the coordinated response system that turns signals into action.

## 4-Level System Explanation Drill

Level 1:

Incident response is how AOIS handles serious failures.

Level 2:

AOIS assigns severity, roles, timeline, communication, mitigation, and review.

Level 3:

When an agent SLO is exhausted, AOIS declares an incident, routes risky actions to human review, freezes risky changes, communicates impact, resolves the active risk, and creates follow-up work.

Level 4:

Incident response connects SLO burn, telemetry, event traces, agent gates, operational roles, communication cadence, mitigation, rollback, and post-incident learning into one reliability control loop.

## Failure Story

The incident agent begins producing vague recommendations during a memory-pressure incident.

The API stays up, but operators lose confidence in the recommendations. Nobody declares an incident because the service appears available. Prompt changes continue while the agent is already degraded.

The result:

- unsafe recommendations stay in the workflow
- operators disagree about severity
- no single person owns coordination
- updates are scattered
- the team later cannot reconstruct the timeline

Fix:

- declare a SEV2 agent-quality incident
- assign an incident commander
- freeze prompt and tool changes
- route low-confidence recommendations to human review
- preserve traces and outputs
- write internal updates
- complete post-incident review with action items

## Mastery Checkpoint

Answer before moving on:

1. What problem does incident response solve in AOIS?
2. Why does v18 come after SLOs?
3. What is the difference between triage and root cause analysis?
4. What does an incident commander do?
5. What does a scribe do?
6. Why does AOIS need an agent operator role?
7. What is mitigation?
8. What is resolution?
9. Why should root cause not be claimed before evidence?
10. What should happen when an agent produces unsafe recommendations during an incident?
11. Why does v18 avoid live pager or chatops tooling?
12. Explain v18 using the 4-layer tool rule.

Answer key:

1. It turns reliability signals into coordinated action.
2. SLOs tell AOIS when reliability is failing; incident response tells operators what to do.
3. Triage classifies impact and urgency quickly; root cause analysis explains why after evidence is gathered.
4. The incident commander coordinates severity, roles, timeline, escalation, and resolution.
5. The scribe records the timeline and important decisions.
6. AI-specific risks need ownership for prompt freezes, tool gates, output review, and safety controls.
7. Mitigation reduces active impact.
8. Resolution means exit criteria are met and active impact is controlled.
9. Premature root cause claims can send responders toward the wrong fix.
10. Route risky outputs to human review, freeze risky changes, preserve evidence, and escalate severity if needed.
11. The lesson teaches coordination without consuming server resources or creating live operational hooks.
12. Human goal: reduce impact and restore trust. Interface: severity, runbooks, channels, updates. Mechanism: roles, lifecycle, escalation, mitigation, review. Substrate: telemetry, traces, SLOs, event streams, logs, and agent outputs.

## Connection Forward

v18 gives AOIS a response model for reliability failures.

v19 moves into chaos engineering: how to test AOIS reliability assumptions safely through tabletop experiments, guardrails, blast-radius control, and no live fault injection.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v18 Introduction](02-introduction.md)
- Next: [v18 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
