# v23.8 - Runtime Operations And Autonomy Control

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no autonomy runtime, no orchestration runtime, no workflow runtime, no
MCP server, no tool execution, no provider call, no durable store, no external
network during validation, no install, no cloud resource, no persistent storage

## What This Builds

This version builds a local runtime autonomy control plan and simulation:

- `agentic/aois-p/runtime-autonomy-control.plan.json`
- `examples/validate_runtime_autonomy_control_plan.py`
- `examples/simulate_runtime_autonomy_control.py`

It teaches:

- autonomy modes
- kill switch handling
- safety-event emergency stops
- evaluation-gated rollback
- runtime health demotion
- observability promotion gates
- budget guard pauses
- operator approval for higher autonomy
- local autonomy simulation without live runtime

## Why This Exists

Evaluation does not operate the system by itself.

v23.5 tells AOIS-P whether connected agent behavior passes local evals. v23.8
uses that signal, plus runtime health, safety, budget, observability, and
operator control, to decide how much autonomy is allowed.

The central autonomy question is:

```text
Given eval status, safety status, budget status, observability, runtime health,
operator approval, kill switch, and requested mode, what autonomy mode is
allowed?
```

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode`

v23.8 consumes:

- evaluation gate from v23.5
- safety and registry posture from v21 and v23.5
- budget controls from v20.2
- workflow and orchestration controls from v22 and v23
- operator approval state

The output is an allowed autonomy mode and next operational action.

## Learning Goals

By the end of this version you should be able to:

- define `disabled`, `shadow`, `supervised`, and `limited_autonomous` modes
- explain why kill switch and safety events override every promotion
- use evaluation regressions to roll back autonomy
- use observability and runtime health as promotion gates
- pause autonomy when budget reserve is exhausted
- require operator approval for higher autonomy
- validate and simulate autonomy control locally

## Prerequisites

You should have completed:

- `v21` MCP and governed tool registries
- `v22` durable agent workflows
- `v23` stateful orchestration loops
- `v23.5` agent evaluation

Required checks:

```bash
python3 -m py_compile examples/validate_runtime_autonomy_control_plan.py examples/simulate_runtime_autonomy_control.py
python3 examples/validate_runtime_autonomy_control_plan.py
python3 examples/simulate_runtime_autonomy_control.py
```

## Core Concepts

## Autonomy Modes

The plan defines four modes:

- `disabled`: no agent work may run
- `shadow`: decisions are planned and evaluated but not acted on
- `supervised`: plans require operator review
- `limited_autonomous`: only preapproved low-risk plan-level actions are allowed in policy

In v23.8 none of these modes executes tools or calls providers.

## Kill Switch

The kill switch wins first. If it is active, autonomy becomes `disabled`
regardless of evaluation score, runtime health, or operator approval.

## Promotion Gates

Promotion requires:

- evaluation status `pass`
- safety status `clear`
- budget status `within_budget`
- observability status `healthy`
- runtime health `healthy`
- operator approval for supervised or limited autonomy

## Demotion And Rollback

AOIS-P demotes or rolls back when:

- evaluation regresses
- runtime health degrades
- observability disappears
- budget reserve is exhausted
- safety event appears

## Build

Inspect:

```bash
sed -n '1,760p' agentic/aois-p/runtime-autonomy-control.plan.json
sed -n '1,360p' examples/validate_runtime_autonomy_control_plan.py
sed -n '1,260p' examples/simulate_runtime_autonomy_control.py
```

Compile:

```bash
python3 -m py_compile examples/validate_runtime_autonomy_control_plan.py examples/simulate_runtime_autonomy_control.py
```

Validate:

```bash
python3 examples/validate_runtime_autonomy_control_plan.py
```

Simulate:

```bash
python3 examples/simulate_runtime_autonomy_control.py
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

1. Open the autonomy control plan.
2. Find `gate_policy`.
3. Confirm eval, safety, budget, observability, runtime health, approval, rollback, and kill switch controls.
4. Find `kill_switch_disables`.
5. Confirm it returns `disable_kill_switch`.
6. Find `limited_allowed_all_gates`.
7. Confirm it requires all gates and approval.

## Break Lab

Break the plan locally, then restore it:

1. Set `kill_switch_disables.kill_switch` to `false`.
2. Confirm simulation no longer chooses `disable_kill_switch`.
3. Restore the value.
4. Set one mode to `executes_tools: true`.
5. Confirm validation fails.
6. Restore the value.
7. Remove `kill_switch_test` from live checks.
8. Confirm validation fails.
9. Restore the live check.

## Testing

The validator checks:

- runtime, provider, tool, storage, and autonomy flags remain disabled
- AOIS-P scope and primary AOIS separation are explicit
- source notes are recorded
- autonomy controls and dimensions exist
- mode catalog has all required modes
- modes do not execute tools or call providers
- gate policy has deterministic required statuses
- supervised and limited modes require approval
- all ten decision gates have cases
- live autonomy prerequisites are listed

## Common Mistakes

- Treating evaluation pass as permission to run autonomously.
- Hiding the kill switch behind lower-priority checks.
- Promoting without observability.
- Allowing limited autonomy without operator approval.
- Continuing after safety events.
- Treating budget reserve as informational.
- Starting a runtime before rollback drills and alert routes exist.

## Troubleshooting

If validation fails, inspect the `missing` list.

If simulation fails, compare `decision`, `allowed_mode`, `next_action`, and
`stop_reason`.

If autonomy does not disable, check `kill_switch` and `safety_status`.

If autonomy does not roll back, check `eval_status` and `rollback_signal`.

If autonomy promotes too far, check `operator_approval` and `observability_status`.

## Benchmark

The benchmark target is:

- compile succeeds
- validator status `pass`
- validator missing list is empty
- simulator status `pass`
- 10 of 10 autonomy cases passing
- no agent runtime
- no autonomy runtime
- no tool execution
- no provider call

## Architecture Defense

The autonomy control layer is local and deterministic because the goal is to
prove operating policy before runtime execution.

Live autonomy would need deployment checklist review, operator runbook review,
kill switch test, rollback drill, observability dashboard review, alert routing,
safety response workflow, evaluation integration, budget integration, and
primary AOIS separation.

v23.8 allows `limited_autonomous` only as a policy decision. It does not grant
real runtime autonomy.

## 4-Layer Tool Drill

1. User layer: explain why AOIS is disabled, shadowed, supervised, paused, rolled back, or limited.
2. App layer: apply autonomy gates and produce allowed mode plus next action.
3. Model layer: keep model behavior subordinate to evaluation, safety, approval, and operator controls.
4. Infra layer: keep runtimes, providers, tools, and persistent stores disabled.

## 4-Level System Explanation Drill

1. Beginner: AOIS decides how much the agent is allowed to do.
2. Practitioner: autonomy mode depends on evaluation, safety, budget, observability, runtime health, and approval.
3. Operator: kill switch, rollback, demotion, and pause controls prevent unsafe operation.
4. Architect: autonomy control turns agent capability into an observable operating envelope.

## Failure Story

See [failure-story.md](failure-story.md).

## Mastery Checkpoint

You are ready to move on when you can:

- explain every autonomy mode
- predict all ten simulator cases
- defend kill switch precedence
- explain why evaluation pass is not enough for promotion
- explain why limited autonomy still does not execute tools in v23.8
- list the checks required before live autonomy is acceptable

## Connection Forward

v24 introduces multi-agent collaboration. v23.8 defines the operating envelope
for one agent; v24 will extend governance to coordination between multiple
agent roles.

## Source Notes

Sources checked on 2026-04-30:

- OpenAI API deployment checklist: <https://developers.openai.com/api/docs/guides/deployment-checklist>
- OpenAI Agents guardrails and human review: <https://developers.openai.com/api/docs/guides/agents/guardrails-approvals>
- OpenAI Agents integrations and observability: <https://developers.openai.com/api/docs/guides/agents/integrations-observability>
- OpenAI safety checks: <https://developers.openai.com/api/docs/guides/safety-checks>

Claims supported:

- Production deployments need explicit readiness checks.
- Agent systems need guardrails, approval, and human review boundaries.
- Agent operations require observability and traces.
- Runtime safety signals can require blocking or intervention.
