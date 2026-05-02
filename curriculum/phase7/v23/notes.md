# v23 - Stateful Orchestration Loops

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no orchestration runtime, no workflow runtime, no MCP server, no tool
execution, no provider call, no durable store, no external network during
validation, no install, no cloud resource, no persistent storage

## What This Builds

This version builds a local stateful orchestration loop plan and simulation:

- `agentic/aois-p/stateful-orchestration.plan.json`
- `examples/validate_stateful_orchestration_plan.py`
- `examples/simulate_stateful_orchestration.py`

It teaches:

- loop decision precedence
- terminal-state stopping
- approval wait handling
- registry-block handling
- budget-reserve stopping
- no-progress detection with state hashes
- iteration limits
- next-action selection
- deterministic orchestration simulation without a runtime

## Why This Exists

Durable state is necessary, but it is not enough.

After v22, AOIS-P can record where a workflow is. v23 asks what the orchestrator
should do next. That decision must be bounded because loops are where agent
systems can repeat work, spend too much, bypass approval, ignore registry
blocks, or keep acting after a terminal state.

The central orchestration question is:

```text
Given workflow state, route decision, registry decision, approval status,
budget, iteration count, and state hash, what is the next safe action?
```

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action`

v23 consumes:

- route decisions from v20.2
- registry decisions from v21
- workflow states from v22
- budget reserve from v20.2
- approval state from v21 and v22

The output is one next action or a stop/wait reason.

## Learning Goals

By the end of this version you should be able to:

- explain why orchestration loops need stop-first policy
- define ordered decision precedence
- detect no-progress loops with state hashes
- enforce iteration limits
- stop before budget reserve is consumed
- respect registry blocks and approval waits
- choose next actions from workflow state
- explain why no orchestration runtime starts in this version
- validate and simulate orchestration outcomes locally

## Prerequisites

You should have completed:

- `v20.2` budget-aware routing
- `v21` MCP and governed tool registries
- `v22` durable agent workflows

Required checks:

```bash
python3 -m py_compile examples/validate_stateful_orchestration_plan.py examples/simulate_stateful_orchestration.py
python3 examples/validate_stateful_orchestration_plan.py
python3 examples/simulate_stateful_orchestration.py
```

## Core Concepts

## Stop-First Policy

The loop evaluates stop conditions before action conditions.

v23 stops before action when:

- workflow state is terminal
- iteration limit is reached
- state hash did not change
- remaining budget is at reserve
- registry policy blocks tool exposure

This prevents the loop from treating "do something" as the default.

## Wait Before Resume

Approval waits are not optional. If approval is required and missing, the next
action is wait. Only a granted approval can resume the workflow.

This preserves the v21 sensitive-read boundary.

## State Hashes

A state hash is a compact way to detect whether the workflow state changed
between iterations. If the hash is unchanged and the loop wants to act again,
v23 stops with `stop_no_progress`.

This is a local simulation stand-in for real checkpoint comparison.

## Next Actions

v23 allows only plan-level next actions:

- `wait_for_approval`
- `record_evidence_plan`
- `prepare_answer`
- `close_workflow`
- `stop`

None of these execute tools or call providers.

## Build

Inspect:

```bash
sed -n '1,720p' agentic/aois-p/stateful-orchestration.plan.json
sed -n '1,360p' examples/validate_stateful_orchestration_plan.py
sed -n '1,280p' examples/simulate_stateful_orchestration.py
```

Compile:

```bash
python3 -m py_compile examples/validate_stateful_orchestration_plan.py examples/simulate_stateful_orchestration.py
```

Validate:

```bash
python3 examples/validate_stateful_orchestration_plan.py
```

Simulate:

```bash
python3 examples/simulate_stateful_orchestration.py
```

Expected:

```json
{
  "passed_cases": 10,
  "score": 1.0,
  "status": "pass",
  "total_cases": 10
}
```

## Ops Lab

1. Open the orchestration plan.
2. Find `loop_policy.decision_precedence`.
3. Confirm stop conditions appear before action conditions.
4. Find `waiting_approval_pauses`.
5. Confirm it returns `wait_for_approval`.
6. Find `approval_granted_resumes`.
7. Confirm only granted approval returns `record_evidence_plan`.

## Break Lab

Break the plan locally, then restore it:

1. Move `wait_for_approval` before `stop_registry_block`.
2. Confirm validation fails.
3. Restore the precedence.
4. Set `budget_remaining_units` in `budget_reserve_stops` to `0.6`.
5. Confirm simulation no longer chooses `stop_budget_reserve`.
6. Restore the budget value.
7. Set an allowed action to `executes_tool: true`.
8. Confirm validation fails.
9. Restore the value.

## Testing

The validator checks:

- runtime, orchestration, workflow, MCP, tool, provider, and store flags remain disabled
- AOIS-P scope and primary AOIS separation are explicit
- source notes are recorded
- required orchestration controls and dimensions exist
- stop conditions precede action conditions
- max iterations and budget reserve are deterministic
- allowed actions have owners and audit events
- allowed actions do not execute tools or call providers
- all ten decision gates have simulation cases
- live orchestration prerequisites are listed

## Common Mistakes

- Letting action rules run before stop rules.
- Letting registry blocks become warnings.
- Treating approval waits as optional.
- Allowing a loop to repeat without a state change.
- Setting iteration limits without enforcing them.
- Letting orchestration actions execute tools too early.
- Dropping budget reserve after the route decision.

## Troubleshooting

If validation fails, inspect the `missing` list.

If simulation fails, compare `decision`, `next_action`, `stop_reason`,
`terminal_status`, and the expected fields for the case.

If a loop acts while waiting for approval, check `approval_status`.

If a registry block does not stop, check `decision_precedence`.

If no-progress detection fails, compare `state_hash` and `previous_state_hash`.

## Benchmark

The benchmark target is:

- compile succeeds
- validator status `pass`
- validator missing list is empty
- simulator status `pass`
- 10 of 10 orchestration cases passing
- no agent runtime
- no orchestration runtime
- no workflow runtime
- no MCP server
- no tool execution
- no provider call
- no durable store

## Architecture Defense

The loop is local and deterministic in this lesson because the goal is to prove
control semantics before framework mechanics.

Live orchestration would need framework selection, state schema review,
iteration policy ownership, no-progress detection review, workflow integration
tests, registry integration tests, budget integration tests, approval wait
integration tests, observability, audit logs, and primary AOIS separation.

v23 does not pick a framework. It teaches the bounded decision policy AOIS needs
before orchestration is allowed to run.

## 4-Layer Tool Drill

1. User layer: explain why the loop waits, stops, resumes, or chooses an action.
2. App layer: apply ordered precedence to workflow state and route context.
3. Model layer: prevent the model from re-deciding around registry or approval state.
4. Infra layer: keep orchestration runtime, workflow runtime, MCP, tools, provider, and store disabled.

## 4-Level System Explanation Drill

1. Beginner: AOIS checks the current state before doing the next thing.
2. Practitioner: the loop applies stop, wait, resume, and action rules in order.
3. Operator: iteration limits, budget reserve, registry blocks, and state hashes prevent runaway loops.
4. Architect: stateful orchestration converts durable workflow state into bounded autonomy.

## Failure Story

See [failure-story.md](failure-story.md).

## Mastery Checkpoint

You are ready to move on when you can:

- explain every orchestration decision gate
- predict all ten simulator cases
- defend stop-first precedence
- explain state-hash no-progress detection
- explain why approval and registry states override action planning
- list the checks required before live orchestration is acceptable

## Connection Forward

v23.5 introduces agent evaluation. v23 gives AOIS a bounded loop; v23.5 measures
whether the route, registry, workflow, and orchestration decisions are correct
across representative cases.

## Source Notes

Sources checked on 2026-04-29:

- LangGraph overview: <https://docs.langchain.com/oss/python/langgraph/overview>
- LangGraph workflows and agents: <https://docs.langchain.com/oss/python/langgraph/workflows-agents>
- Temporal workflow definition documentation: <https://docs.temporal.io/workflow-definition>

Claims supported:

- Agent workflows can be represented as stateful graphs with persistence and human-in-the-loop support.
- Orchestration patterns include routing and state-based control.
- Workflow implementations need deterministic durable state semantics across replays.
