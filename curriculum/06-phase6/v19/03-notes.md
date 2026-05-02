# v19 - Chaos Engineering Without Fault Injection

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: chaos engineering plan and tabletop simulation only, no fault injection, no load test, no network fault, no CPU stress, no memory stress, no pod delete, no agent runtime, no provider call

## What This Builds

This version builds a chaos engineering plan:

- `chaos/aois-p/chaos-engineering.plan.json`
- `examples/validate_chaos_engineering_plan.py`
- `examples/simulate_chaos_game_day.py`

It teaches:

- chaos engineering purpose
- steady state
- hypothesis
- blast radius
- guardrails
- abort conditions
- rollback conditions
- game-day roles
- tabletop simulation
- agent failure scenarios
- why chaos must protect the primary AOIS project

## Why This Exists

v18 gave AOIS incident response maturity.

The next question is proactive:

```text
Can AOIS safely test whether its response model works before a real incident?
```

Chaos engineering answers that question, but it can be dangerous if used
carelessly. On a shared server with a primary AOIS workload, live chaos must not
start without explicit approval, resource limits, blast-radius review, and abort
conditions.

v19 therefore teaches the discipline first through plan validation and tabletop
simulation only.

## AOIS Connection

The AOIS path is now:

`telemetry -> tracing -> event streaming -> SLOs -> incident response -> chaos engineering`

Chaos engineering uses all earlier layers:

- telemetry confirms steady state
- traces explain request and agent paths
- event streaming exposes lag and replay behavior
- SLOs define acceptable impact
- incident response defines what operators do when the experiment reveals weakness

In AOIS, chaos also includes AI-specific failure modes:

- unsafe recommendation
- low-quality recommendation
- missing evidence before action
- tool permission risk
- provider or model degradation

## Learning Goals

By the end of this version you should be able to:

- explain chaos engineering without treating it as random breakage
- define steady state
- write a chaos hypothesis
- define blast radius
- define abort conditions
- explain why SLO budget must be checked before experiments
- explain why the primary AOIS project is excluded
- design an agent-failure tabletop exercise
- validate a chaos plan locally
- run a local game-day simulation without injecting faults

## Prerequisites

You should have completed:

- `v16` unified telemetry
- `v16.5` agent and incident tracing
- `v17` event streaming
- `v17.5` service and agent SLOs
- `v18` incident response maturity

Required checks:

```bash
python3 -m py_compile examples/validate_chaos_engineering_plan.py examples/simulate_chaos_game_day.py
python3 examples/validate_chaos_engineering_plan.py
python3 examples/simulate_chaos_game_day.py
```

## Core Concepts

## Chaos Engineering

Chaos engineering is controlled experimentation used to discover system
weakness before uncontrolled failure discovers it for you.

It is not:

- randomly breaking production
- running stress tools without limits
- deleting pods to look advanced
- creating failures without a hypothesis
- testing on a shared primary workload without approval

Good chaos engineering is careful, measured, reversible, and scoped.

## Steady State

Steady state is the normal behavior you expect before the experiment.

Examples:

- API latency is inside SLO
- event consumer lag is inside SLO
- agent recommendation quality is inside SLO
- primary AOIS workload is healthy
- memory and disk have safe headroom

If steady state is already broken, you do not run chaos. You already have an
incident or operational risk.

## Hypothesis

A hypothesis predicts what should happen during the experiment.

Bad hypothesis:

```text
Break the API and see what happens.
```

Good hypothesis:

```text
If API latency increases, operators detect SLO burn, declare the right severity,
and follow the incident response runbook.
```

The goal is learning, not damage.

## Blast Radius

Blast radius defines how far the experiment can affect the system.

For v19, blast radius is intentionally limited to:

- local plan review
- tabletop simulation
- synthetic incident discussion
- no live infrastructure mutation

Before live chaos, blast radius must specify exactly which service, users,
resources, and dependencies can be affected.

## Abort Condition

An abort condition says when to stop.

Examples:

- primary AOIS is touched
- SLO budget is unavailable
- memory or disk headroom is unsafe
- a live provider call would be needed
- the experiment requires destructive action
- the incident commander says stop

Abort conditions must be defined before the experiment starts.

## Rollback

Rollback returns the system to safe state.

In v19, rollback is simple because no runtime is changed:

```text
discard simulation notes or restore the local plan file
```

In live chaos, rollback must be specific, tested, and owned.

## Game Day

A game day is a planned exercise where operators rehearse a failure scenario.

Game days need:

- owner
- observer
- scribe
- timebox
- pre-brief
- abort word
- communication plan
- post-review

## Agent Chaos

Agent chaos tests AI-specific reliability assumptions.

Examples:

- agent recommends unsafe action
- agent gives vague remediation
- agent loses required evidence
- agent tries to use a risky tool
- agent quality SLO is exhausted

In v19, these are tabletop scenarios only. No provider call, tool call, or
destructive action is executed.

## Build

Inspect:

```bash
sed -n '1,340p' chaos/aois-p/chaos-engineering.plan.json
sed -n '1,340p' examples/validate_chaos_engineering_plan.py
sed -n '1,260p' examples/simulate_chaos_game_day.py
```

Compile:

```bash
python3 -m py_compile examples/validate_chaos_engineering_plan.py examples/simulate_chaos_game_day.py
```

Validate:

```bash
python3 examples/validate_chaos_engineering_plan.py
```

Simulate:

```bash
python3 examples/simulate_chaos_game_day.py
```

Expected validation:

```json
{
  "chaos_runtime_started": false,
  "fault_injection_executed": false,
  "load_test_started": false,
  "network_fault_started": false,
  "cpu_stress_started": false,
  "memory_stress_started": false,
  "pod_delete_executed": false,
  "agent_runtime_started": false,
  "provider_call_made": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

Expected simulation:

- API latency game day is approved for tabletop only
- stream lag game day is approved for tabletop only
- agent bad-recommendation game day is blocked because SLO budget is unavailable and an abort condition is seen
- no fault injection or runtime action occurs

## Ops Lab

Answer from the plan and simulator:

1. What is the namespace?
2. Which field proves no fault injection occurred?
3. Which field proves no load test started?
4. Which field proves no pod delete occurred?
5. Which experiment is blocked in the simulator?
6. Why is it blocked?
7. What is the blast radius for v19?
8. Why is primary AOIS excluded?

Answer key:

1. `aois-p`
2. `fault_injection_executed=false`
3. `load_test_started=false`
4. `pod_delete_executed=false`
5. `aois-p-agent-bad-recommendation-game-day`
6. SLO budget is unavailable and an abort condition is seen.
7. Local plan review and tabletop simulation only.
8. The primary project has priority and must not be risked by a secondary curriculum exercise.

## Break Lab

Use a scratch copy or reversible local edit only.

### Option A - Enable Fault Injection

Set:

```json
"fault_injection_executed": true
```

Expected validator result:

- `fault_injection_executed_must_be_false`

Risk:

- a lesson becomes an unapproved live chaos experiment.

### Option B - Remove Abort Condition

Remove `abort_condition` from one experiment.

Expected validator result:

- `experiment_missing_field:abort_condition:<experiment-name>`

Risk:

- responders do not know when to stop.

### Option C - Approve Live Execution

Set an experiment:

```json
"approved_for_live_execution": true
```

Expected validator result:

- `experiment_must_not_be_live:<experiment-name>`

Risk:

- live chaos is approved without blast-radius, SLO, resource, and primary-project review.

## Testing

Run:

```bash
python3 -m py_compile examples/validate_chaos_engineering_plan.py examples/simulate_chaos_game_day.py
python3 examples/validate_chaos_engineering_plan.py
python3 examples/simulate_chaos_game_day.py
```

Pass criteria:

- scripts compile
- validator status is `pass`
- simulator status is `pass`
- all runtime and fault flags are false
- one experiment is blocked by guardrails
- no live infrastructure action occurs

## Common Mistakes

Mistake 1: Confusing chaos engineering with random destruction.

Correction: chaos is controlled experimentation with hypothesis, guardrails,
blast radius, and rollback.

Mistake 2: Running chaos while steady state is already broken.

Correction: if steady state is broken, treat it as an incident or operational
risk first.

Mistake 3: Ignoring resource constraints.

Correction: on the shared server, chaos must not consume memory, disk, CPU, or
primary-project capacity without explicit approval.

Mistake 4: Testing agents like normal APIs only.

Correction: AI agents need quality, safety, evidence, and tool-permission
failure scenarios.

Mistake 5: Running experiments without abort conditions.

Correction: abort conditions are part of the experiment design, not an
afterthought.

## Troubleshooting

If validation fails:

1. Confirm every runtime and fault flag is false.
2. Confirm namespace is `aois-p`.
3. Confirm each experiment name starts with `aois-p-`.
4. Confirm each experiment has hypothesis, steady state, blast radius, abort condition, rollback, SLO guardrail, and agent guardrail.
5. Confirm each experiment has `approved_for_live_execution=false`.
6. Confirm game-day policy has owner, observer, scribe, pre-brief, post-review, abort word, timebox, and primary-project exclusion.
7. Confirm all limits are zero.
8. Confirm required live-chaos checks are listed.

If simulation fails:

1. Confirm the plan file exists.
2. Confirm experiment names match the simulator inputs.
3. Confirm the blocked experiment still has unavailable SLO budget or an abort condition.

## Benchmark

Record:

- validator status
- simulator status
- runtime services started
- fault injections executed
- experiment count
- blocked experiment count
- repo size
- `.venv` size
- memory available

This benchmark proves chaos design discipline, not live fault-injection power.

## Architecture Defense

Defend these choices:

1. v19 does not inject faults because the shared server has a primary workload and no approved blast radius.
2. Chaos starts with steady state because experiments against an already-broken system confuse learning with incident response.
3. SLO budget is checked before experiments because reliability margin determines whether extra risk is acceptable.
4. Agent chaos is included because AI failure modes include bad recommendations, risky tool use, and missing evidence.
5. One experiment is blocked intentionally because safe chaos engineering must say no when guardrails fail.
6. Live chaos requires explicit approval, communication, abort, rollback, and post-review.

## 4-Layer Tool Drill

Explain chaos engineering through the 4-layer tool rule:

1. Human goal: discover reliability weaknesses before they become uncontrolled incidents.
2. Interface: chaos plan, game-day checklist, simulator output, review notes.
3. Mechanism: steady state, hypothesis, blast radius, guardrails, abort, rollback, review.
4. Substrate: telemetry, traces, SLOs, event streams, runbooks, infrastructure, agent outputs.

Answer key:

Chaos engineering is not the fault-injection tool. The tool is only an interface. The mechanism is disciplined experimentation under safety controls.

## 4-Level System Explanation Drill

Level 1:

Chaos engineering safely tests whether AOIS can handle failures.

Level 2:

AOIS defines steady state, forms a hypothesis, limits blast radius, and simulates or runs a controlled experiment.

Level 3:

If guardrails pass, AOIS can run a tabletop game day. If SLO budget is unavailable or primary AOIS might be touched, the experiment is blocked.

Level 4:

Chaos engineering connects observability, SLOs, incident response, agent safety, resource constraints, and post-review into a proactive reliability learning loop.

## Failure Story

A team decides to "test resilience" by running a memory stress command on the shared server.

They do not define steady state, do not check SLO budget, do not exclude primary AOIS, and do not define abort conditions. The server is already under memory pressure.

The result:

- primary AOIS becomes unstable
- OOM risk increases
- the team cannot tell whether the result came from the experiment or existing pressure
- no useful learning is captured

Fix:

- stop treating chaos as random stress
- declare or investigate existing memory pressure first
- protect primary AOIS
- write a tabletop experiment
- define steady state, hypothesis, blast radius, abort, and rollback
- run live chaos only after explicit approval

## Mastery Checkpoint

Answer before moving on:

1. What problem does chaos engineering solve in AOIS?
2. Why is chaos not random breakage?
3. What is steady state?
4. What is a chaos hypothesis?
5. What is blast radius?
6. What is an abort condition?
7. Why must SLO budget be checked before chaos?
8. Why is primary AOIS excluded from v19 experiments?
9. Why does v19 include agent chaos?
10. Why is one simulator experiment blocked?
11. Why does v19 avoid live fault injection?
12. Explain v19 using the 4-layer tool rule.

Answer key:

1. It discovers reliability weaknesses before uncontrolled incidents reveal them.
2. It is controlled experimentation with hypothesis, guardrails, blast radius, abort, and rollback.
3. Steady state is the normal expected system behavior before an experiment.
4. A prediction about what should happen during a controlled failure scenario.
5. The allowed scope of impact.
6. A pre-defined condition that stops the experiment.
7. If the budget is exhausted, the system has no reliability margin for added risk.
8. The primary project has priority and must not be endangered by this curriculum.
9. AI systems fail through quality, safety, evidence, and tool-permission problems, not only infrastructure outages.
10. The agent experiment has unavailable SLO budget and an abort condition.
11. No blast radius, resource, or live-change approval exists, and the server is shared.
12. Human goal: discover weakness safely. Interface: plan, checklist, simulator, review. Mechanism: steady state, hypothesis, blast radius, abort, rollback. Substrate: telemetry, SLOs, traces, events, infrastructure, and agent outputs.

## Connection Forward

v19 teaches safe failure experimentation.

v19.5 moves from general chaos engineering into AI failure engineering and governance enforcement: policy boundaries, agent action gates, unsafe-output handling, and controls that stop autonomous systems from crossing operational limits.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19 Introduction](02-introduction.md)
- Next: [v19 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
