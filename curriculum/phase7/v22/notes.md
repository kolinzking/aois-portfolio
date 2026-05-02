# v22 - Durable Agent Workflows

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no workflow runtime, no MCP server, no tool execution, no provider
call, no durable store, no external network during validation, no install, no
cloud resource, no persistent storage

## What This Builds

This version builds a local durable agent workflow plan and simulation:

- `agentic/aois-p/durable-workflow.plan.json`
- `examples/validate_durable_workflow_plan.py`
- `examples/simulate_durable_workflow.py`

It teaches:

- workflow state machines
- checkpoints and terminal states
- pause and resume for human approval
- route and registry context propagation
- idempotency keys
- bounded retries
- step timeouts
- recovery actions
- deterministic workflow simulation without a runtime

## Why This Exists

Agent work often spans more than one step. It may need to route, check the tool
registry, wait for approval, record evidence, prepare an answer, and close.

If that process is only in memory, it can fail in dangerous ways:

- an approval wait is lost
- a retry repeats a side effect
- a timeout leaves the incident ambiguous
- a registry block is bypassed after restart
- a user cannot tell what happened

Durable workflow design gives AOIS-P a recoverable state model before live
workflow infrastructure exists.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve agent workflow state`

v22 carries forward:

- route decisions from v20.2
- registry decisions from v21
- approval boundaries from v21
- cost context from v20.1 and v20.2

The result is a workflow contract that can pause, resume, block, complete, or
time out without losing the reason.

## Learning Goals

By the end of this version you should be able to:

- explain why agent workflows need durable state
- distinguish checkpoints from logs
- define terminal and non-terminal workflow states
- explain how approval waits resume safely
- use idempotency keys to avoid duplicate work
- bound retries and timeouts
- map registry denials to blocked workflow states
- explain why no workflow runtime starts in this version
- validate and simulate durable workflow outcomes locally

## Prerequisites

You should have completed:

- `v20.1` step cost accounting
- `v20.2` budget-aware routing
- `v21` MCP and governed tool registries

Required checks:

```bash
python3 -m py_compile examples/validate_durable_workflow_plan.py examples/simulate_durable_workflow.py
python3 examples/validate_durable_workflow_plan.py
python3 examples/simulate_durable_workflow.py
```

## Core Concepts

## Durable State

Durable state means the workflow can resume from recorded progress after an
interruption. In v22, durable state is represented as a plan and simulation.

Live systems might use a workflow engine and durable storage. AOIS-P does not
start either in this lesson.

## Checkpoints

A checkpoint records what step finished, with the inputs and outputs needed to
resume safely.

A log explains what happened. A checkpoint controls what can happen next.

## Approval Waits

Approval waits are workflow states, not comments. The workflow must be able to
say:

- approval is not required
- approval is required and missing
- approval is granted
- approval timed out

v22 models both pause and resume paths.

## Idempotency

Retries and restarts can repeat a step. Idempotency keys let AOIS-P detect that
a step was already checkpointed and skip duplicate work.

This matters before live tools exist because the same pattern will be required
when future workflows execute side-effecting operations.

## Retry And Timeout Policy

Every retry needs a budget. Every wait needs a timeout. Every terminal state
needs a recovery action.

v22 records these policies in the workflow plan and proves them with eight
simulation cases.

## Build

Inspect:

```bash
sed -n '1,620p' agentic/aois-p/durable-workflow.plan.json
sed -n '1,360p' examples/validate_durable_workflow_plan.py
sed -n '1,260p' examples/simulate_durable_workflow.py
```

Compile:

```bash
python3 -m py_compile examples/validate_durable_workflow_plan.py examples/simulate_durable_workflow.py
```

Validate:

```bash
python3 examples/validate_durable_workflow_plan.py
```

Simulate:

```bash
python3 examples/simulate_durable_workflow.py
```

Expected:

```json
{
  "passed_cases": 8,
  "score": 1.0,
  "status": "pass",
  "total_cases": 8
}
```

## Ops Lab

1. Open the workflow plan.
2. Find `sensitive_trace_waits_for_approval`.
3. Confirm the registry decision is `require_human_approval`.
4. Confirm approval is `required_missing`.
5. Confirm the simulator returns `waiting_for_approval`.
6. Compare it to `approval_checkpoint_resumes`.
7. Explain what changed between pause and resume.

## Break Lab

Break the plan locally, then restore it:

1. Remove `timed_out` from terminal states.
2. Confirm validation fails.
3. Restore `timed_out`.
4. Set a step timeout to a negative number.
5. Confirm validation fails.
6. Restore the timeout.
7. Change the duplicate idempotency case to `idempotency_key_seen: false`.
8. Confirm simulation no longer selects `skip_duplicate_step`.
9. Restore the value.

## Testing

The validator checks:

- runtime, workflow, MCP, provider, and durable-store flags remain disabled
- AOIS-P scope and primary AOIS separation are explicit
- source notes are recorded
- workflow controls are present
- workflow dimensions are present
- state machine includes terminal states and transitions
- every step has owner, inputs, outputs, checkpoint, idempotency, timeout, retry, and compensation fields
- all eight decision gates have simulation cases
- live workflow prerequisites are listed

## Common Mistakes

- Treating logs as checkpoints.
- Retrying without idempotency.
- Waiting for approval without a timeout.
- Letting registry-denied tools continue in a later step.
- Treating timeout as an exception instead of a terminal state.
- Starting a workflow engine before resource and persistence design exists.
- Dropping cost and registry context after the route step.

## Troubleshooting

If validation fails, inspect the `missing` list.

If simulation fails, compare `decision`, `state`, `terminal_status`,
`recovery_action`, and the expected fields for the case.

If approval does not pause, check `registry_decision` and `approval_status`.

If a timeout does not win, check `elapsed_seconds` and `timeout_seconds`.

If duplicate work is not skipped, check `idempotency_key_seen`.

## Benchmark

The benchmark target is:

- compile succeeds
- validator status `pass`
- validator missing list is empty
- simulator status `pass`
- 8 of 8 workflow cases passing
- no agent runtime
- no workflow runtime
- no durable store
- no MCP server
- no tool execution
- no provider call

## Architecture Defense

The workflow is local and deterministic in this lesson because the goal is to
prove state semantics before runtime mechanics.

Live workflow execution would need engine selection, durable store sizing,
checkpoint schema review, approval UX, timeout policy, retry policy,
observability, audit logs, route integration tests, registry integration tests,
and primary AOIS separation.

v22 does not choose Temporal or LangGraph. It teaches the durable concepts AOIS
needs before a runtime decision.

## 4-Layer Tool Drill

1. User layer: explain whether the workflow is complete, waiting, blocked, retried, timed out, or skipped.
2. App layer: validate checkpoints, idempotency, retry budgets, and terminal states.
3. Model layer: preserve route and registry context across steps instead of re-deciding from scratch.
4. Infra layer: keep workflow runtime, durable store, MCP, tools, and provider execution disabled.

## 4-Level System Explanation Drill

1. Beginner: AOIS remembers where the agent left off.
2. Practitioner: each workflow step records a checkpoint and can pause or resume.
3. Operator: retries, timeouts, approvals, and registry blocks have explicit recovery paths.
4. Architect: durable workflows turn one-shot agent actions into auditable state machines.

## Failure Story

See [failure-story.md](failure-story.md).

## Mastery Checkpoint

You are ready to move on when you can:

- explain every workflow decision gate
- predict all eight simulator cases
- defend the difference between logs and checkpoints
- explain how approval wait and resume work
- explain why idempotency comes before live tool execution
- list the checks required before live workflow runtime is acceptable

## Connection Forward

v23 introduces stateful orchestration loops. v22 preserves workflow state; v23
will use that state to choose the next bounded action until the workflow is
complete, blocked, waiting, failed, or timed out.

## Source Notes

Sources checked on 2026-04-29:

- Temporal documentation: <https://docs.temporal.io/>
- LangGraph durable execution documentation: <https://docs.langchain.com/oss/python/langgraph/durable-execution>
- Model Context Protocol specification: <https://modelcontextprotocol.io/specification/>

Claims supported:

- Durable workflow systems preserve progress across interruptions.
- Checkpointed graph execution can support pause, resume, and human-in-the-loop behavior.
- Workflow tool steps must preserve MCP host, server, and tool boundaries from v21.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v22 Introduction](introduction.md)
- Next: [v22 Lab](lab.md)
<!-- AOIS-NAV-END -->
