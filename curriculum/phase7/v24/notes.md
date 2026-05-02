# v24 - Multi-Agent Collaboration

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no multi-agent runtime, no autonomy runtime, no orchestration runtime,
no workflow runtime, no MCP server, no tool execution, no provider call, no
durable store, no external network during validation, no install, no cloud
resource, no persistent storage

## What This Builds

This version builds a governed multi-agent collaboration plan and simulation:

- `agentic/aois-p/multi-agent-collaboration.plan.json`
- `examples/validate_multi_agent_collaboration_plan.py`
- `examples/simulate_multi_agent_collaboration.py`

It teaches:

- supervisor-owned routing
- specialist role catalogs
- handoff contracts
- shared state ownership
- context filtering
- conflict escalation
- handoff loop limits
- shadow-mode collaboration holds
- local multi-agent simulation without a live multi-agent framework

## Why This Exists

More agents do not automatically mean more reliability.

Once AOIS-P has tool plans, budgets, registry controls, workflow state,
orchestration, evaluation, and autonomy modes, the next risk is coordination.
Multiple agents can duplicate work, pass stale context, hide ownership, create
conflicting findings, or bounce a case between specialists until the operator
loses the thread.

The central collaboration question is:

```text
Given current agent, requested target, autonomy mode, handoff count, context
freshness, safety status, budget status, and conflict status, should AOIS-P
handoff, block, hold, stop, or escalate?
```

v24 answers that question without starting a live agent runtime.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles`

v24 consumes:

- runtime autonomy mode from v23.8
- connected evaluation posture from v23.5
- orchestration state from v23
- durable workflow state from v22
- registry and safety posture from v21
- budget posture from v20.2

The output is a collaboration decision, next agent, next action, and audit path.

## Learning Goals

By the end of this version you should be able to:

- explain why a supervisor must own multi-agent routing
- define role catalogs for specialists
- distinguish handoff metadata from shared application state
- prevent parallel specialists from corrupting one shared state object
- block stale context and unknown targets
- stop handoff loops
- escalate conflicting specialist findings to a human operator
- connect autonomy mode to collaboration permission
- validate and simulate collaboration policy locally

## Prerequisites

You should have completed:

- `v21` MCP and governed tool registries
- `v22` durable agent workflows
- `v23` stateful orchestration loops
- `v23.5` agent evaluation
- `v23.8` runtime operations and autonomy control

Required checks:

```bash
python3 -m py_compile examples/validate_multi_agent_collaboration_plan.py examples/simulate_multi_agent_collaboration.py
python3 examples/validate_multi_agent_collaboration_plan.py
python3 examples/simulate_multi_agent_collaboration.py
```

## Core Concepts

## Supervisor

The supervisor is the only role allowed to route work to specialists. It owns
the shared state, commits specialist patches, and records the audit event.

## Specialist Roles

v24 defines four specialist roles:

- `evidence_agent`: plans missing evidence collection
- `safety_agent`: reviews unsafe or sensitive action paths
- `budget_agent`: checks cost and budget posture
- `response_agent`: synthesizes the final approved response

It also defines `human_operator` for conflict escalation.

## Handoff Contract

A handoff must include:

- reason
- priority
- state summary
- requested output

The receiving role gets minimal role-scoped context. Handoff metadata is not a
replacement for durable workflow state or registry policy.

## Shared State

The supervisor owns the shared state. Specialists return findings or patches.
They do not commit state directly in v24.

This avoids split-brain updates when two specialists see different versions of
the same incident.

## Autonomy Gate

Shadow mode records the proposed collaboration but does not transfer control.
Supervised mode can route to specialists. Limited autonomy remains policy-only
in this lesson and still performs no tool calls.

## Loop Limit

An incident can have at most four handoffs in the local simulation. When the
limit is reached, AOIS-P stops and reviews the loop instead of continuing.

## Build

Inspect:

```bash
sed -n '1,760p' agentic/aois-p/multi-agent-collaboration.plan.json
sed -n '1,360p' examples/validate_multi_agent_collaboration_plan.py
sed -n '1,260p' examples/simulate_multi_agent_collaboration.py
```

Compile:

```bash
python3 -m py_compile examples/validate_multi_agent_collaboration_plan.py examples/simulate_multi_agent_collaboration.py
```

Validate:

```bash
python3 examples/validate_multi_agent_collaboration_plan.py
```

Simulate:

```bash
python3 examples/simulate_multi_agent_collaboration.py
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

1. Open the collaboration plan.
2. Find `role_catalog`.
3. Confirm every role has an owner, allowed targets, and no provider/tool capability.
4. Find `handoff_contract`.
5. Confirm required payload fields, context filtering, loop limit, and serial handoffs.
6. Find `shared_state_contract`.
7. Confirm the supervisor owns state and conflicts escalate to an operator.
8. Find `collaboration_cases`.
9. Confirm every decision gate has a case.

## Break Lab

Break the plan locally, then restore it:

1. Remove `response_agent` from the supervisor allowed targets.
2. Confirm validation fails or simulation blocks the final handoff.
3. Restore the target.
4. Set `parallel_handoffs_allowed` to `true`.
5. Confirm validation fails.
6. Restore the value.
7. Change `shadow_mode_holds_collaboration.autonomy_mode` to `supervised`.
8. Confirm simulation no longer returns `hold_autonomy_mode`.
9. Restore the value.

## Testing

The validator checks:

- runtime, multi-agent, provider, tool, storage, and autonomy flags stay disabled
- AOIS-P scope and primary AOIS separation are explicit
- source notes are recorded
- collaboration scope controls exist
- required governance controls exist
- role catalog includes supervisor, specialists, and operator escalation
- roles have owners and cannot execute tools or call providers
- handoff contract requires payload fields and serial execution
- shared state is supervisor-owned
- all ten decision gates have cases
- live multi-agent prerequisites are listed

## Common Mistakes

- Treating multi-agent as a quality improvement by default.
- Letting specialists write shared state directly.
- Passing full incident context to every role.
- Allowing parallel handoffs before conflict policy exists.
- Forgetting that handoff tools are still control surfaces.
- Letting shadow mode transfer control.
- Continuing after a handoff loop reaches its limit.
- Escalating conflicts back to another model instead of an operator.

## Troubleshooting

If validation fails:

- inspect the `missing` list
- check source note URLs and dates
- confirm all runtime flags are false
- confirm all required roles exist
- confirm each role has `may_execute_tools: false`
- confirm each role has `may_call_provider: false`

If simulation fails:

- compare `decision` to `expected_decision`
- check the priority order in `_decide`
- confirm `current_agent` can route to `requested_target`
- confirm shadow mode, loop limit, stale context, parallel request, and conflict cases are not masked

## Benchmark

Pass criteria:

- validator status is `pass`
- simulator status is `pass`
- simulator score is `1.0`
- all ten collaboration cases pass
- no runtime, tool, provider, storage, or network flag is enabled

## Architecture Defense

Defend this design:

AOIS-P does not start a multi-agent runtime in v24 because collaboration changes
ownership, context, and failure modes. The first milestone is proving that
handoffs are allowed only through a supervisor, specialists have explicit
owners, context is scoped, conflicts escalate, and loops stop.

## 4-Layer Tool Drill

Use the AOIS tool boundary lens:

1. Product layer: what operational job needs a specialist?
2. Policy layer: which role is allowed to receive this handoff?
3. Runtime layer: what state, context, and audit event move with it?
4. Failure layer: how does AOIS-P block, stop, or escalate?

## 4-Level System Explanation Drill

Explain v24 at four levels:

1. Beginner: one supervisor sends work to specialists only when rules allow it.
2. Operator: every handoff needs owner, reason, context, loop count, and audit event.
3. Engineer: the simulator turns case fields into deterministic route, block, hold, stop, or escalate decisions.
4. Architect: multi-agent collaboration is a state-management and governance problem before it is a model-orchestration problem.

## Failure Story

A team adds a second agent to "double-check" incident evidence. The evidence
agent sees an old trace, the safety agent sees a newer registry decision, and
the response agent synthesizes both without knowing they conflict. The final
recommendation appears confident but is based on mismatched state.

v24 prevents this by making the supervisor own shared state, blocking stale
context, disallowing parallel specialist commits, and escalating conflicts to a
human operator.

## Mastery Checkpoint

You have mastered v24 when you can:

- draw the role catalog from memory
- explain why `human_operator` is a role in the plan
- explain why shadow mode holds collaboration
- add a new specialist role without allowing tool execution
- add a new case and update the simulator expectation
- defend why the supervisor commits state

## Connection Forward

v25 moves from multi-agent coordination to safe execution boundaries. After
AOIS-P can decide who should work on a case, it must define which actions can be
executed, which require approval, which must be sandboxed, and which remain
plan-only.

## Source Notes

Checked 2026-05-02.

- Model Context Protocol specification, version 2025-11-25: used for current tool, resource, prompt, consent, and tool-safety boundaries.
- LangGraph overview documentation: used for stateful, long-running, human-in-the-loop agent orchestration concepts.
- OpenAI API tools documentation: used for current tool, function-calling, and MCP integration vocabulary.
- v24 remains a local AOIS-P collaboration contract. It does not start a framework runtime, MCP server, hosted tool, provider call, or external network path.
