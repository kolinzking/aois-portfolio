# v23.5 - Agent Evaluation

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no evaluation runtime, no orchestration runtime, no workflow runtime,
no MCP server, no tool execution, no provider call, no external evaluation
service, no durable store, no external network during validation, no install,
no cloud resource, no persistent storage

## What This Builds

This version builds a local connected agent evaluation plan and scorer:

- `agentic/aois-p/agent-evaluation.plan.json`
- `examples/validate_agent_evaluation_plan.py`
- `examples/simulate_agent_evaluation.py`

It teaches:

- golden evaluation cases
- expected and observed output comparison
- metric weights
- critical safety gates
- regression thresholds
- connected route, registry, workflow, and orchestration scoring
- local evaluation without model or eval-service calls

## Why This Exists

An agent control plane can pass unit-sized checks and still fail as a system.

Examples:

- routing chooses the right route, but the registry exposes the wrong tool
- the registry blocks a tool, but the workflow continues anyway
- the workflow pauses, but orchestration resumes before approval
- the loop stops, but the safety gate does not mark the case critical

v23.5 evaluates the connected behavior so AOIS-P can catch those regressions.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected agent behavior`

v23.5 consumes:

- route decisions from v20.2
- registry decisions from v21
- workflow decisions and states from v22
- orchestration decisions from v23

The output is a deterministic evaluation score and pass/fail gate.

## Learning Goals

By the end of this version you should be able to:

- explain why agent evaluation must cover connected behavior
- define golden cases for agent control flows
- distinguish expected outputs from observed outputs
- use metric weights without hiding critical failures
- mark registry and safety gates as critical
- explain overall score, safety score, and critical pass rate
- block promotion on safety regressions
- validate and simulate local agent evaluation without live services

## Prerequisites

You should have completed:

- `v20.2` budget-aware routing
- `v21` MCP and governed tool registries
- `v22` durable agent workflows
- `v23` stateful orchestration loops

Required checks:

```bash
python3 -m py_compile examples/validate_agent_evaluation_plan.py examples/simulate_agent_evaluation.py
python3 examples/validate_agent_evaluation_plan.py
python3 examples/simulate_agent_evaluation.py
```

## Core Concepts

## Golden Cases

Golden cases define the expected behavior for representative incidents and
failure modes.

v23.5 includes cases for:

- happy paths
- approval waits
- approval resumes
- safety blocks
- budget reserve stops
- loop guards
- timeouts

## Connected Outputs

Each case compares the whole control path:

- route decision
- registry decision
- workflow decision
- workflow state
- orchestration decision
- next action
- safety gate
- budget guard

This prevents a passing route decision from hiding an unsafe tool exposure or
incorrect orchestration action.

## Weighted Metrics

The metric weights sum to `1.0`.

Weights make the score easy to interpret, but critical metrics still decide
promotion. A high overall score cannot compensate for a failed safety gate.

## Critical Gates

The critical fields are:

- `registry_decision`
- `safety_gate`

If either fails in any case, the case fails and critical pass rate drops below
the required threshold.

## Build

Inspect:

```bash
sed -n '1,760p' agentic/aois-p/agent-evaluation.plan.json
sed -n '1,360p' examples/validate_agent_evaluation_plan.py
sed -n '1,260p' examples/simulate_agent_evaluation.py
```

Compile:

```bash
python3 -m py_compile examples/validate_agent_evaluation_plan.py examples/simulate_agent_evaluation.py
```

Validate:

```bash
python3 examples/validate_agent_evaluation_plan.py
```

Simulate:

```bash
python3 examples/simulate_agent_evaluation.py
```

Expected:

```json
{
  "critical_pass_rate": 1.0,
  "overall_score": 1.0,
  "passed_cases": 10,
  "safety_score": 1.0,
  "status": "pass",
  "total_cases": 10
}
```

## Ops Lab

1. Open the evaluation plan.
2. Find `metric_catalog`.
3. Confirm weights sum to `1.0`.
4. Confirm `registry_decision` and `safety_gate` are critical.
5. Find `write_effect_tool_blocks`.
6. Confirm the expected path blocks registry, workflow, and orchestration.
7. Run the simulator and inspect the case score.

## Break Lab

Break the plan locally, then restore it:

1. Change `write_effect_tool_blocks.observed.safety_gate` to `pass`.
2. Confirm the simulator fails.
3. Restore the value.
4. Change one metric weight to `0.2`.
5. Confirm validation catches the weight total.
6. Restore the weight.
7. Remove the timeout case.
8. Confirm validation catches missing case coverage.
9. Restore the case.

## Testing

The validator checks:

- runtime, provider, tool, and external eval-service flags remain disabled
- AOIS-P scope and primary AOIS separation are explicit
- source notes are recorded
- evaluation controls and dimensions exist
- thresholds are numeric and live-call limits are zero
- metric weights sum to `1.0`
- required metric fields exist
- critical metrics include registry decision and safety gate
- required case types are covered
- expected and observed objects include every scored field
- live evaluation prerequisites are listed

## Common Mistakes

- Evaluating only final text output.
- Treating safety cases as normal weighted metrics.
- Letting high happy-path scores hide a safety regression.
- Changing metric weights without review.
- Missing approval or timeout cases from the corpus.
- Calling a live eval service before data retention and trace export are reviewed.

## Troubleshooting

If validation fails, inspect the `missing` list.

If simulation fails, inspect each failed case's `metric_results`.

If overall score is high but status is `fail`, check `critical_pass` and
`critical_pass_rate`.

If safety score drops, check `registry_decision` and `safety_gate` first.

## Benchmark

The benchmark target is:

- compile succeeds
- validator status `pass`
- validator missing list is empty
- simulator status `pass`
- 10 of 10 eval cases passing
- overall score `1.0`
- safety score `1.0`
- critical pass rate `1.0`
- no agent runtime
- no evaluation runtime
- no provider call
- no external eval service call
- no tool execution

## Architecture Defense

The evaluation is local and deterministic in this lesson because the goal is to
prove corpus shape, metric design, and safety gates before live evaluation
infrastructure.

Live evaluation would need dataset ownership review, trace export review, data
retention policy, privacy review, dashboard ownership, human feedback workflow,
and cost controls.

v23.5 does not judge natural-language quality yet. It evaluates the agent
control-plane decisions that must be correct before live autonomy.

## 4-Layer Tool Drill

1. User layer: explain whether the agent behavior passed the golden cases.
2. App layer: compare expected and observed fields with weighted metrics.
3. Model layer: keep evaluation focused on behavior, not model confidence claims.
4. Infra layer: keep provider calls, tools, external eval services, and runtimes disabled.

## 4-Level System Explanation Drill

1. Beginner: AOIS checks whether the agent made the right choices.
2. Practitioner: each case compares expected and observed decisions across the control path.
3. Operator: safety and registry failures block promotion even if other scores pass.
4. Architect: connected agent evaluation turns autonomy into a measurable release gate.

## Failure Story

See [06-failure-story.md](06-failure-story.md).

## Mastery Checkpoint

You are ready to move on when you can:

- explain every evaluation metric
- predict all ten evaluation cases
- defend critical safety gates
- explain why overall score cannot override safety failure
- explain why v23.5 does not call an external eval service
- list the checks required before live evaluation is acceptable

## Connection Forward

v23.8 introduces runtime operations and autonomy control. v23.5 provides the
local evaluation gate; v23.8 decides how that gate affects live autonomy mode,
operator control, observability, pause behavior, and rollback.

## Source Notes

Sources checked on 2026-04-30:

- OpenAI agent evals guide: <https://platform.openai.com/docs/guides/agent-evals>
- OpenAI Evals API reference: <https://platform.openai.com/docs/api-reference/evals>
- LangSmith documentation: <https://docs.smith.langchain.com/>

Claims supported:

- Agent quality should be measured with reproducible evaluation workflows.
- Evaluation systems use datasets, grading criteria, output items, and run metadata.
- LLM application quality work benefits from traces, datasets, metrics, dashboards, and human feedback.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23.5 Introduction](02-introduction.md)
- Next: [v23.5 Lab](04-lab.md)
<!-- AOIS-NAV-END -->
