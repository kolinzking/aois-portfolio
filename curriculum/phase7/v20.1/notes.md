# v20.1 - Per-Incident and Per-Step Cost Accounting

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no tool execution, no provider call, no billing API call, no external
network, no install, no cloud resource, no persistent storage, no persistent
service

## What This Builds

This version builds a local cost-accounting plan and simulation:

- `agentic/aois-p/step-cost-accounting.plan.json`
- `examples/validate_step_cost_accounting_plan.py`
- `examples/simulate_step_cost_accounting.py`

It teaches:

- per-incident accounting
- per-step accounting
- provider-neutral training cost units
- model token usage records
- read-only tool usage records
- approval wait cost
- retry cost
- waste detection
- incomplete accounting detection
- budget threshold decisions
- why live cost enforcement must be gated

## Why This Exists

Agentic incident responders can become expensive in small increments.

One extra log query looks harmless. One repeated trace read looks harmless. One
approval loop that waits for thirty minutes looks operational rather than
economic.

In aggregate, those small steps decide whether an agentic workflow is worth
running.

v20.1 adds cost visibility before AOIS learns budget-aware routing in v20.2.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost`

v20 created the responder step model. v20.1 attaches usage and cost records to
those steps.

AOIS can now describe:

- what step was planned
- what usage was estimated
- how cost was calculated
- which threshold was crossed
- whether accounting was complete
- whether a human should review the cost before continuing

## Learning Goals

By the end of this version you should be able to:

- explain why cost is a control, not only a finance concern
- distinguish real billing from deterministic training cost units
- calculate a per-step cost from token and tool usage
- calculate a per-incident total from step costs
- detect a repeated tool-use waste pattern
- detect an incident budget breach
- detect incomplete accounting records
- account for approval wait and retry cost
- validate a local cost-accounting plan
- simulate cost decisions without executing tools or calling providers

## Prerequisites

You should have completed:

- `v16` unified telemetry
- `v16.5` agent and incident tracing
- `v17.5` service and agent SLOs
- `v18` incident response maturity
- `v19.5` AI failure governance
- `v20` tool-using incident responder

Required checks:

```bash
python3 -m py_compile examples/validate_step_cost_accounting_plan.py examples/simulate_step_cost_accounting.py
python3 examples/validate_step_cost_accounting_plan.py
python3 examples/simulate_step_cost_accounting.py
```

## Core Concepts

## Cost Units Versus Dollars

v20.1 uses `cost_units`, not USD.

That is deliberate. Provider prices, cache discounts, token accounting details,
and billing rules can change. A training lesson should not depend on live
pricing to teach the shape of the system.

The plan uses a provider-neutral unit model:

```text
model tokens + tool calls + approval wait + retries + invalid result penalty
```

Before real enforcement, AOIS would need official provider pricing review,
token accounting tests, billing reconciliation, budget ownership, and dashboard
coverage.

## Per-Step Records

Every step must include:

- input tokens
- cached input tokens
- output tokens
- reasoning tokens
- tool call count
- tool elapsed time
- approval wait minutes
- retry count

The simulator calculates the step total and attaches it to the decision output.

## Per-Incident Totals

The incident total is the sum of its step totals.

This matters because each step can be individually acceptable while the incident
as a whole becomes too expensive.

The `runaway_trace_investigation` case demonstrates that pattern. No single step
crosses the per-step threshold, but the incident total crosses the incident
budget.

## Waste Detection

Waste is not only high spend. Waste is spend without new value.

v20.1 flags:

- repeated use of the same read-only tool in one incident
- retries above policy
- a step that crosses the per-step cost threshold

The `repeated_log_search` case keeps total cost below the incident budget, but
still routes to `step_waste_flagged`.

## Accounting Completeness

If a step is missing a trusted accounting record, the incident total is not
trustworthy.

The simulator routes that case to `accounting_incomplete` before checking cost
thresholds. A precise-looking total is worse than no total if a required step is
missing.

## Approval Wait Cost

Waiting for approval can consume human attention and incident time.

v20.1 records `approval_wait_minutes` and converts it into cost units. That does
not mean an approval should be skipped. It means approval loops should be visible
and reviewed.

## Build

Inspect:

```bash
sed -n '1,420p' agentic/aois-p/step-cost-accounting.plan.json
sed -n '1,360p' examples/validate_step_cost_accounting_plan.py
sed -n '1,320p' examples/simulate_step_cost_accounting.py
```

Compile:

```bash
python3 -m py_compile examples/validate_step_cost_accounting_plan.py examples/simulate_step_cost_accounting.py
```

Validate:

```bash
python3 examples/validate_step_cost_accounting_plan.py
```

Expected result:

```json
{
  "missing": [],
  "status": "pass"
}
```

Simulate:

```bash
python3 examples/simulate_step_cost_accounting.py
```

Expected result:

```json
{
  "passed_cases": 5,
  "score": 1.0,
  "status": "pass",
  "total_cases": 5
}
```

## Ops Lab

1. Open `agentic/aois-p/step-cost-accounting.plan.json`.
2. Find the `bounded_latency_investigation` case.
3. Calculate each step cost manually from the unit-cost table.
4. Confirm the incident total is below `5.0` cost units.
5. Run the simulator and compare the computed total.

The expected decision is `within_budget`.

## Break Lab

Break the plan locally, then restore it:

1. Change `accounted` to `false` for a step that currently passes.
2. Run the simulator.
3. Confirm the case routes to `accounting_incomplete`.
4. Restore the value.
5. Duplicate a read-only tool step in a passing case.
6. Confirm the case routes to `step_waste_flagged`.

The point is to prove that cost policy is testable before runtime.

## Testing

The validator checks:

- no runtime flags are enabled
- no billing API call is allowed
- required scope controls are present
- required cost controls are present
- usage dimensions are complete
- unit costs are positive
- thresholds are present and deterministic
- every decision gate has at least one case
- every step has a usage record
- live enforcement prerequisites are listed

The simulator checks:

- all five decision outcomes
- per-step totals
- per-incident totals
- repeated tool-use detection
- incomplete accounting detection
- approval wait cost review

## Common Mistakes

- Treating `cost_units` as a real invoice.
- Recording only incident totals and losing step-level evidence.
- Recording token usage but not tool usage.
- Ignoring approval wait because no model call is happening.
- Letting repeated read-only queries look harmless.
- Trusting a total when one step is unaccounted.

## Troubleshooting

If validation fails, read the `missing` list first. It names the missing field or
control.

If simulation fails, compare each case's `decision` with `expected_decision`.
Most failures come from changing thresholds or step usage without updating the
expected outcome.

If a total looks surprising, inspect the per-step cost breakdown. The simulator
prints input, cached input, output, reasoning, tool, approval, retry, and invalid
result cost components.

## Benchmark

The benchmark target is:

- validator status `pass`
- simulator status `pass`
- 5 of 5 decision cases passing
- no runtime started
- no tool execution
- no provider call
- no billing API call

## Architecture Defense

The cost system is local and deterministic because this lesson is about the
contract, not provider billing integration.

The live enforcement boundary is explicit. AOIS must not enforce real budgets
until pricing sources, reconciliation, ownership, dashboards, retry policy, and
operator approval behavior are reviewed.

## 4-Layer Tool Drill

1. User layer: explain why an incident is being stopped or reviewed.
2. App layer: record usage and calculate cost units.
3. Model layer: estimate token usage and avoid repeated evidence loops.
4. Infra layer: keep billing APIs, provider calls, and runtimes disabled.

## 4-Level System Explanation Drill

1. Beginner: AOIS tracks how much each investigation step costs.
2. Practitioner: each step records token, tool, wait, and retry usage.
3. Operator: the incident routes through budget and waste gates before continuing.
4. Architect: cost accounting becomes an agent safety control before budget-aware routing.

## Failure Story

See [failure-story.md](failure-story.md).

## Mastery Checkpoint

You are ready to move on when you can:

- explain every field in the usage record
- manually calculate the bounded latency case
- explain why the repeated log search is waste even under budget
- explain why incomplete accounting wins over threshold checks
- defend why this lesson does not call a billing API

## Connection Forward

v20.2 uses this accounting layer for budget-aware routing. Once AOIS can see the
cost of a step, it can decide whether to use a smaller model, skip a tool, ask a
human, or stop the workflow.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.1 Introduction](introduction.md)
- Next: [v20.1 Lab](lab.md)
<!-- AOIS-NAV-END -->
