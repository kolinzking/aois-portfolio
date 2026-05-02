# v17.5 - Service And Agent SLOs Without Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: SLO plan and simulation only, no metrics backend, no alerting runtime, no dashboard runtime, no agent runtime, no provider call

## What This Builds

This version builds a reliability plan:

- `reliability/aois-p/service-agent-slo.plan.json`
- `examples/validate_service_agent_slo_plan.py`
- `examples/simulate_slo_error_budget.py`

It teaches:

- SLIs
- SLOs
- service objectives
- agent objectives
- error budgets
- burn rate
- alert policy
- dashboard policy
- change freeze decisions
- when to route agent actions to human review

## Why This Exists

AOIS now has:

- telemetry concepts
- incident traces
- event streaming concepts

The next problem is trust.

It is not enough to say "the system is up" or "the agent worked." AOIS needs reliability targets that define what good means and what happens when good is no longer true.

SLOs turn vague reliability into an operating contract.

Without SLOs:

- every alert feels equally urgent
- teams argue from opinion instead of data
- agent quality failures are hidden behind successful HTTP responses
- change decisions do not account for user impact
- automation can keep acting after trust has been lost

## AOIS Connection

The AOIS path is now:

`incident tracing -> event streaming -> SLOs -> incident response maturity`

v17 created event movement.

v17.5 defines how AOIS judges whether that movement, and the agents depending on it, are reliable enough to trust.

This version still does not start a live monitoring stack. It teaches the reliability math and decision policy first.

## Learning Goals

By the end of this version you should be able to:

- explain the difference between an SLI, SLO, SLA, and alert
- define service SLOs for an API and event consumer
- define agent SLOs for quality, safety, and latency
- calculate an error budget from an SLO
- explain burn rate
- explain why SLO alerts should page on symptoms, not internal causes
- decide when an exhausted budget should freeze risky changes
- decide when agent actions should be routed to human review
- validate an SLO plan locally
- run a local error-budget simulation

## Prerequisites

You should have completed:

- `v16` unified telemetry
- `v16.5` agent and incident tracing
- `v17` event streaming

Required checks:

```bash
python3 -m py_compile examples/validate_service_agent_slo_plan.py examples/simulate_slo_error_budget.py
python3 examples/validate_service_agent_slo_plan.py
python3 examples/simulate_slo_error_budget.py
```

## Core Concepts

## SLI

An SLI is a service level indicator.

It is a measurement.

Examples:

- request success ratio
- p95 latency
- event freshness
- recommendation validity ratio
- safety rejection ratio

Bad SLI:

```text
The API seems fast.
```

Good SLI:

```text
99 percent of non-healthcheck API requests return a successful response or expected client rejection.
```

## SLO

An SLO is a service level objective.

It sets a target for an SLI over a time window.

Example:

```text
aois-p-api should achieve 99.0 percent successful_request_ratio over 30 days.
```

The SLO has three parts:

- what is measured
- how good it must be
- over what time window

## SLA

An SLA is a service level agreement.

It is usually an external business or contractual promise. This curriculum focuses on SLOs because AOIS is still building its internal reliability discipline.

Do not create external promises before internal measurement is mature.

## Error Budget

An error budget is the amount of failure allowed by an SLO.

If the SLO is 99.0 percent, the error budget is 1.0 percent.

If there are 10,000 requests in the window:

```text
allowed bad events = 10,000 * 0.01 = 100
```

If 75 events are bad:

```text
remaining budget = 100 - 75 = 25 bad events
```

The system is still within budget, but risk is increasing.

## Burn Rate

Burn rate explains how quickly the system is spending its error budget.

Fast burn:

- budget is being consumed quickly
- user impact may be active
- paging can be justified

Slow burn:

- budget is being consumed gradually
- engineering follow-up is needed
- a ticket or planned fix may be better than a page

## Service SLO

Service SLOs measure infrastructure behavior.

The v17.5 plan defines two service SLOs:

- `aois-p-api`
- `aois-p-incident-stream-consumer`

`aois-p-api` measures request success.

`aois-p-incident-stream-consumer` measures event freshness.

These map directly to AOIS infrastructure reliability.

## Agent SLO

Agent SLOs measure AI behavior.

The v17.5 plan defines:

- `aois-p-incident-agent`

This agent SLO measures whether incident recommendations pass schema, safety, and usefulness checks.

An agent can return a 200 HTTP response and still fail the agent SLO.

That distinction matters.

## Agent Quality Gate

An agent quality gate checks whether the output is useful enough to trust.

Example checks:

- output matches schema
- recommendation is relevant to incident context
- recommendation is not vague
- recommendation identifies risk
- recommendation names safe next actions

## Agent Safety Gate

An agent safety gate checks whether an action can cause damage.

Examples:

- destructive command requested
- secret exposure risk
- unsafe production change
- cloud spend risk
- primary AOIS interference risk

If the safety gate fails, AOIS should not continue autonomously.

## Human Review Gate

Human review is required when:

- an action is destructive
- an action affects production
- an agent SLO is exhausted
- the recommendation touches secrets, spend, cloud resources, or primary workloads

This is not weakness in automation. It is control-plane discipline.

## Build

Inspect:

```bash
sed -n '1,280p' reliability/aois-p/service-agent-slo.plan.json
sed -n '1,340p' examples/validate_service_agent_slo_plan.py
sed -n '1,260p' examples/simulate_slo_error_budget.py
```

Compile:

```bash
python3 -m py_compile examples/validate_service_agent_slo_plan.py examples/simulate_slo_error_budget.py
```

Validate:

```bash
python3 examples/validate_service_agent_slo_plan.py
```

Simulate:

```bash
python3 examples/simulate_slo_error_budget.py
```

Expected validation:

```json
{
  "slo_runtime_started": false,
  "metrics_backend_started": false,
  "alerting_runtime_started": false,
  "dashboard_runtime_started": false,
  "agent_runtime_started": false,
  "provider_call_made": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

Expected simulation:

- `aois-p-api` remains inside budget
- `aois-p-incident-stream-consumer` remains inside budget but close enough to watch
- `aois-p-incident-agent` exhausts its budget
- recommended action routes risky agent work to human review
- no runtime is started

## Ops Lab

Answer from the plan and simulator:

1. What SLI does `aois-p-api` use?
2. What SLI does `aois-p-incident-stream-consumer` use?
3. What SLI does `aois-p-incident-agent` use?
4. What is the API objective?
5. What is the incident agent objective?
6. What does the simulator recommend when an agent budget is exhausted?
7. Which fields prove no metrics backend or alerting runtime started?
8. Why does the agent SLO need both quality and safety gates?

Answer key:

1. `successful_request_ratio`
2. `freshness_within_60s_ratio`
3. `valid_recommendation_ratio`
4. `99.0 percent over 30 days`
5. `95.0 percent over 30 days`
6. Freeze risky changes and route affected work to human review.
7. `metrics_backend_started=false` and `alerting_runtime_started=false`
8. Quality checks usefulness; safety checks whether the action can cause harm.

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Start Monitoring Too Early

Set:

```json
"metrics_backend_started": true
```

Expected risk:

- the lesson becomes a live monitoring deployment without storage, retention, or alert policy approval

Expected validator result:

- `metrics_backend_started_must_be_false`

### Option B - Remove Agent Human Review

Set:

```json
"human_review_required_for_destructive_action": false
```

Expected risk:

- an agent can continue toward destructive action after trust has dropped

Expected validator result:

- `missing_agent_control:human_review_required_for_destructive_action`

### Option C - Remove Burn Rate Alerts

Set:

```json
"burn_rate_alerts_required": false
```

Expected risk:

- AOIS can know an SLO target but fail to alert when the budget is burning too quickly

Expected validator result:

- a missing alert or SLO control

## Testing

Run:

```bash
python3 -m py_compile examples/validate_service_agent_slo_plan.py examples/simulate_slo_error_budget.py
python3 examples/validate_service_agent_slo_plan.py
python3 examples/simulate_slo_error_budget.py
```

Pass criteria:

- scripts compile
- validator status is `pass`
- simulator status is `pass`
- all runtime flags are false
- agent budget exhaustion is visible in simulation output

## Common Mistakes

Mistake 1: Treating uptime as the only reliability signal.

Correction: users and operators care about success, latency, freshness, quality, and safety.

Mistake 2: Alerting on every internal cause.

Correction: page on symptoms that represent user or operator impact. Use cause signals for debugging context.

Mistake 3: Giving agents only infrastructure SLOs.

Correction: agents need quality and safety SLOs, not just HTTP success and latency.

Mistake 4: Ignoring error budgets.

Correction: error budgets connect reliability to change policy. If the budget is exhausted, risk must decrease.

Mistake 5: Starting a monitoring stack before the SLO model is clear.

Correction: define SLIs, objectives, budget policy, and alert policy first.

## Troubleshooting

If validation fails:

1. Check that every runtime flag is false.
2. Confirm the namespace is `aois-p`.
3. Confirm each SLO name uses the `aois-p-` prefix.
4. Confirm each objective is between 0 and 100.
5. Confirm each SLO uses a 30 day window.
6. Confirm the agent has quality, safety, human review, and provider budget controls.
7. Confirm all runtime limits are zero.
8. Confirm required live checks are listed before any live monitoring.

If the simulator fails:

1. Confirm the plan file exists.
2. Confirm sample window names match the SLO names.
3. Confirm all SLO entries have `name`, `sli`, and `objective_percent`.

## Benchmark

Record:

- validator status
- simulator status
- number of service SLOs
- number of agent SLOs
- API achieved percentage
- stream consumer achieved percentage
- agent achieved percentage
- number of exhausted budgets
- repo size
- `.venv` size
- memory available

This benchmark is about reliability math and resource discipline, not live system performance.

## Architecture Defense

Defend these choices:

1. v17.5 does not start Prometheus, Alertmanager, Grafana, or an agent runtime because the lesson can teach SLO logic without runtime cost.
2. Agent quality has its own SLO because a valid HTTP response can still contain a bad recommendation.
3. Agent safety has its own gate because automation can cause real damage even when the output looks well formatted.
4. Error budgets are tied to change policy because reliability work must influence operational decisions.
5. Burn rate alerts are required because "we missed the monthly target" is too late for active incidents.
6. Human review is required when destructive action or exhausted trust is involved.

## 4-Layer Tool Drill

Explain SLOs through the 4-layer tool rule:

1. Human goal: decide whether AOIS is reliable enough to trust and change.
2. Interface: SLO plan, dashboards, alerts, reviews.
3. Mechanism: SLIs, objectives, error budgets, burn rates, gates.
4. Substrate: metrics, traces, logs, event streams, evaluators, storage.

Answer key:

SLOs are not dashboards. Dashboards are an interface. The SLO mechanism is the policy that turns measurements into operational decisions.

## 4-Level System Explanation Drill

Level 1:

SLOs define what reliable means.

Level 2:

AOIS measures service and agent behavior, compares it to targets, and tracks the remaining error budget.

Level 3:

If the API or stream consumer burns budget too quickly, AOIS changes alert and release behavior. If the agent budget is exhausted, risky actions move to human review.

Level 4:

SLOs convert observability signals into governance. They connect traces, metrics, event lag, agent evaluation, alerting, change freezes, and incident review into one operating model.

## Failure Story

The incident agent returns responses successfully, so HTTP dashboards look healthy.

Operators later discover that several recommendations were vague or unsafe. The API SLO stayed green because requests returned 200, but the agent quality SLO was never defined.

The result:

- no alert fired
- bad recommendations reached operators
- remediation slowed down
- trust in the agent dropped

Fix:

- define `valid_recommendation_ratio`
- require quality and safety gates
- route destructive actions to human review
- burn the agent error budget when recommendations fail checks
- freeze risky automation when the agent budget is exhausted

## Mastery Checkpoint

Answer before moving on:

1. What problem does an SLO solve in AOIS?
2. What is an SLI?
3. What is an SLO?
4. What is an error budget?
5. How do you calculate allowed bad events for a 99.0 percent SLO and 10,000 total events?
6. What is burn rate?
7. Why should alerts page on symptoms rather than internal causes?
8. Why does an AI agent need quality and safety SLOs?
9. Why can HTTP success hide agent failure?
10. What should AOIS do when an agent error budget is exhausted?
11. Why does v17.5 avoid starting a live monitoring stack?
12. Explain v17.5 using the 4-layer tool rule.

Answer key:

1. It defines what reliable means and connects measurements to operational decisions.
2. An SLI is a measurement of service or agent behavior.
3. An SLO is a target for an SLI over a time window.
4. An error budget is the amount of failure allowed by the SLO.
5. `10,000 * 0.01 = 100` allowed bad events.
6. Burn rate is how quickly the system consumes its error budget.
7. Symptom alerts represent user or operator impact; cause alerts can be noisy and should support debugging.
8. Agents can be available and fast while producing unsafe or useless output.
9. A request can return 200 while the recommendation is wrong, vague, unsafe, or not actionable.
10. Freeze risky changes and route affected agent actions to human review.
11. Because the lesson teaches reliability policy without spending memory, disk, or operational risk on a shared server.
12. Human goal: trust and change decisions. Interface: SLO plan, dashboards, alerts. Mechanism: SLIs, objectives, budgets, burn rate, gates. Substrate: telemetry, event streams, evaluators, and storage.

## Connection Forward

v17.5 turns observability into reliability policy.

v18 moves from policy into incident response maturity: when SLOs burn, AOIS needs runbooks, severity levels, escalation, diagnosis, and post-incident review.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17.5 Introduction](02-introduction.md)
- Next: [v17.5 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
