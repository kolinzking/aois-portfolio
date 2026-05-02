# v10.5 - Managed Agent Tradeoffs Without Creating Agents

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: tradeoff plan and validation only, no cloud agent, no credentials, no provider calls

## What This Builds

This version builds a managed-agent tradeoff plan:

- `cloud/aws/managed-agent-tradeoff.plan.json`
- `examples/validate_managed_agent_plan.py`

It compares:

- AOIS-owned agent runtime
- managed cloud agent placeholder

It teaches:

- orchestration ownership
- tool permission boundaries
- auditability
- vendor coupling
- rollback planning
- why managed agent creation is gated

## Why This Exists

Managed cloud agents can accelerate development, but they can also hide execution details.

AOIS needs to decide what should be owned by the system and what can safely be delegated to a provider.

## AOIS Connection

The AOIS path is now:

`managed model plan -> agent ownership decision -> tool permissions -> auditability -> future managed agent option`

`v10` planned provider inference.
`v10.5` asks whether the agent loop itself should be cloud-managed or AOIS-owned.

## Learning Goals

By the end of this version you should be able to:

- explain managed agent services
- compare managed agent versus owned runtime
- explain tool permission risk
- explain auditability tradeoffs
- explain vendor coupling
- validate the tradeoff plan locally
- explain why managed agent creation is gated

## Resource Gate

Do not create:

- cloud agents
- action groups
- knowledge bases
- tool integrations
- provider credentials
- cloud network calls

Allowed:

- inspect plan JSON
- run local validator

Live managed-agent work requires official docs review, credential plan, budget approval, tool-permission review, data-boundary review, eval baseline, and rollback plan.

## Prerequisites

You should have completed `v10`.

Required checks:

```bash
python3 -m py_compile examples/validate_managed_agent_plan.py
python3 examples/validate_managed_agent_plan.py
```

## Core Concepts

## Managed Agent

A managed agent service hosts parts of the agent loop for you.

It may manage:

- orchestration
- tool calls
- memory or knowledge retrieval
- model invocation
- execution traces

## AOIS-Owned Agent Runtime

AOIS-owned runtime means the agent loop is implemented and observed inside AOIS.

This gives more control but more engineering burden.

## Tool Permission Boundary

Agents become risky when they can use tools.

Before a managed agent can use tools, AOIS needs a clear permission model.

## Auditability

Auditability means you can explain what happened, why, and with what inputs/tools.

Managed services may expose audit data differently from self-owned runtime.

## Vendor Coupling

Vendor coupling is dependence on one provider's agent format, tools, runtime, and logs.

## Build

Inspect:

```bash
sed -n '1,240p' cloud/aws/managed-agent-tradeoff.plan.json
sed -n '1,220p' examples/validate_managed_agent_plan.py
```

Compile:

```bash
python3 -m py_compile examples/validate_managed_agent_plan.py
```

Run:

```bash
python3 examples/validate_managed_agent_plan.py
```

Expected:

```json
{
  "cloud_agent_created": false,
  "credentials_used": false,
  "status": "pass"
}
```

## Ops Lab

Answer:

1. Which option is recommended for the current portfolio?
2. Which option has higher vendor coupling?
3. Which requirement covers tool permissions?
4. Which field proves no cloud agent was created?
5. Which field proves credentials were not used?

Answer key:

1. `aois-owned-agent-runtime`
2. `managed-cloud-agent-placeholder`
3. `tool_permission_review`
4. `cloud_agent_created=false`
5. `credentials_used=false`

## Break Lab

Do not skip this.

### Option A - Choose Managed Agent Too Early

In a scratch copy, set current choice to managed cloud agent.

Expected risk:

- orchestration moves outside AOIS before audit, tool permission, and rollback controls exist

### Option B - Remove Tool Permission Review

In a scratch copy, remove `tool_permission_review`.

Expected risk:

- agent tools may be granted without a clear permission boundary

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. cloud agent created remains false
4. credentials used remains false
5. current choice remains AOIS-owned
6. managed-agent prerequisites are listed

## Common Mistakes

- treating managed agents as simple model calls
- granting tool permissions before policy exists
- accepting provider logs as complete auditability
- ignoring vendor coupling
- creating managed agents before budget and rollback approval

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_managed_agent_plan.py
```

Read `missing`, inspect the plan JSON, and restore required controls.

If live managed-agent use is requested:

- stop
- check official provider docs
- define tool permissions
- define budget
- define credentials and secrets handling
- define rollback plan
- get explicit approval

## Benchmark

Measure:

- validator compile result
- validator status
- current choice
- cloud agent created status
- credentials used status
- repo disk footprint
- memory snapshot

## Architecture Defense

Why keep AOIS-owned runtime for now?

Because the curriculum needs inspectable execution before delegating orchestration to a provider.

Why not create a managed agent?

Because managed agents can invoke tools, cost money, use credentials, and hide runtime details behind provider abstractions.

Why compare tradeoffs now?

Because future enterprise work should choose managed services deliberately, not by default.

## 4-Layer Tool Drill

Tool: managed agent service

1. Plain English
It lets a cloud provider run part of the agent workflow.

2. System Role
It could replace or augment AOIS-owned orchestration later.

3. Minimal Technical Definition
It is a provider-managed runtime for model/tool orchestration, memory/retrieval, and action execution.

4. Hands-on Proof
The validator confirms the tradeoff plan keeps current choice AOIS-owned and creates no cloud agent.

## 4-Level System Explanation Drill

1. Simple English
AOIS can compare managed agents without creating one.

2. Practical Explanation
I can inspect tradeoffs and explain why the current runtime remains AOIS-owned.

3. Technical Explanation
`v10.5` adds a managed-agent tradeoff plan and local validator.

4. Engineer-Level Explanation
AOIS now separates managed-agent evaluation from managed-agent execution, preserving auditability, tool-permission review, budget controls, and rollback requirements before cloud orchestration is delegated.

## Failure Story

Representative failure:

- Symptom: a managed agent calls a tool with unclear permission
- Root cause: tool permission review was skipped before agent creation
- Fix: remove the managed agent path until permissions and rollback are defined
- Prevention: validate the tradeoff plan and keep AOIS-owned runtime until controls exist
- What this taught me: agent orchestration is a trust boundary

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v10.5` solve in AOIS?
2. What is a managed agent?
3. What is AOIS-owned agent runtime?
4. Why is tool permission review required?
5. What is auditability?
6. What is vendor coupling?
7. Why is current choice AOIS-owned?
8. Why is managed agent creation gated?
9. What must exist before managed-agent use?
10. Explain managed agent service using the 4-layer tool rule.
11. Explain `v10.5` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v10.5` solve in AOIS?

It compares cloud-managed agents with AOIS-owned orchestration before creating any cloud agent.

2. What is a managed agent?

A provider-managed runtime for model/tool orchestration and related agent behavior.

3. What is AOIS-owned agent runtime?

An agent loop implemented and observed inside AOIS rather than delegated to a provider.

4. Why is tool permission review required?

Agents can act through tools, so permissions must be explicit before execution.

5. What is auditability?

The ability to explain what happened, why, with which inputs, tools, and outputs.

6. What is vendor coupling?

Dependence on provider-specific runtimes, formats, logs, and integrations.

7. Why is current choice AOIS-owned?

It keeps behavior inspectable while the curriculum builds trust boundaries.

8. Why is managed agent creation gated?

It can involve credentials, tools, cost, data exposure, and provider-side runtime behavior.

9. What must exist before managed-agent use?

Official docs review, credential plan, budget approval, data-boundary review, tool permission review, eval baseline, and rollback plan.

10. Explain managed agent service using the 4-layer tool rule.

- Plain English: it lets a cloud provider run agent behavior.
- System Role: it can replace or augment AOIS orchestration.
- Minimal Technical Definition: it is a provider-managed model/tool orchestration runtime.
- Hands-on Proof: the validator confirms no cloud agent is created and AOIS-owned runtime remains current choice.

11. Explain `v10.5` using the 4-level system explanation rule.

- Simple English: AOIS compares agent ownership choices.
- Practical explanation: I can explain why managed agents are gated.
- Technical explanation: `v10.5` adds a tradeoff plan and validator.
- Engineer-level explanation: AOIS now evaluates managed-agent delegation without giving up auditability, tool-permission control, budget discipline, or rollback planning.

## Connection Forward

`v10.5` defines agent ownership tradeoffs.

`v11` moves to event-driven cloud workflow planning, where AOIS compares serverless orchestration to its local/API workflow.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v10.5 Introduction](02-introduction.md)
- Next: [v10.5 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
