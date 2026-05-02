# v20.2 - Budget-Aware Routing

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no agent
runtime, no routing runtime, no tool execution, no provider call, no billing API
call, no external network, no install, no cloud resource, no persistent storage,
no persistent service

## What This Builds

This version builds a local budget-aware routing plan and simulation:

- `agentic/aois-p/budget-aware-routing.plan.json`
- `examples/validate_budget_aware_routing_plan.py`
- `examples/simulate_budget_aware_routing.py`

It teaches:

- route selection before spend
- confidence-based tool skipping
- model downgrade and no-tool routes
- read-only evidence routing
- severity-based budget limits
- remaining-budget reserves
- expected value to cost checks
- human review for expensive non-high-severity branches
- stop conditions when budget is exhausted
- blocking routing when accounting is incomplete

## Why This Exists

Cost accounting is reactive unless it changes the next route.

v20.1 showed the cost of each step. v20.2 asks whether the next step is worth
taking at all.

The central routing question is:

```text
Given severity, evidence, confidence, value, cost, and remaining budget,
what should AOIS do next?
```

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget`

Budget-aware routing turns cost from a report into an operational control.

AOIS can now choose:

- a small no-tool route when evidence is complete
- a read-only evidence route when evidence is missing but bounded
- human budget review when a branch is useful but expensive
- stop when budget reserve is exhausted
- full read-only investigation when high severity justifies it

## Learning Goals

By the end of this version you should be able to:

- explain why routing should happen before spend
- distinguish accounting from routing
- define a remaining-budget reserve
- use confidence to skip unnecessary tool calls
- use severity to allow or constrain expensive routes
- compare expected value against estimated cost
- identify when human budget review is required
- block routing when the cost ledger is incomplete
- validate a local routing plan
- simulate routing decisions without starting a runtime

## Prerequisites

You should have completed:

- `v20` tool-using incident responder
- `v20.1` per-incident and per-step cost accounting

Required checks:

```bash
python3 -m py_compile examples/validate_budget_aware_routing_plan.py examples/simulate_budget_aware_routing.py
python3 examples/validate_budget_aware_routing_plan.py
python3 examples/simulate_budget_aware_routing.py
```

## Core Concepts

## Accounting Versus Routing

Accounting answers what was consumed.

Routing answers what should happen next.

v20.2 does not replace v20.1. It depends on v20.1. If the cost ledger is
incomplete, routing is blocked because the router cannot trust its inputs.

## Candidate Routes

The plan defines four route types:

- `small_model_no_tool`
- `read_only_evidence`
- `full_investigation`
- `human_budget_review`

The simulator also returns `stop` and `blocked` when policy says no route should
continue.

## Confidence-Based Tool Skipping

If evidence is complete and confidence is high, the safe route is often the cheap
route.

The `confident_low_severity_summary` case proves this: AOIS uses a small no-tool
route instead of spending on another read-only query.

## Severity-Based Budget Limits

Low-severity incidents should not consume the same budget shape as high-severity
outages.

v20.2 sets deterministic route limits for low, medium, and high severity. High
severity can use a full investigation route when the expected value justifies the
cost and the remaining budget can preserve a reserve.

## Human Budget Review

Medium incidents can still have expensive useful routes. v20.2 does not blindly
stop those routes. It pauses them for human budget review when they cross the
expensive-branch threshold.

## Stop Conditions

Budget-aware routing needs explicit stop conditions:

- remaining budget is below reserve
- no route fits the budget
- no route has enough value for its cost
- accounting is incomplete

## Build

Inspect:

```bash
sed -n '1,440p' agentic/aois-p/budget-aware-routing.plan.json
sed -n '1,360p' examples/validate_budget_aware_routing_plan.py
sed -n '1,300p' examples/simulate_budget_aware_routing.py
```

Compile:

```bash
python3 -m py_compile examples/validate_budget_aware_routing_plan.py examples/simulate_budget_aware_routing.py
```

Validate:

```bash
python3 examples/validate_budget_aware_routing_plan.py
```

Simulate:

```bash
python3 examples/simulate_budget_aware_routing.py
```

Expected:

```json
{
  "passed_cases": 6,
  "score": 1.0,
  "status": "pass",
  "total_cases": 6
}
```

## Ops Lab

1. Open the routing plan.
2. Find `confident_low_severity_summary`.
3. Compare the small no-tool route against the read-only and full routes.
4. Confirm the simulator chooses `route_small_model_no_tool`.
5. Explain why the cheapest route is also the right route.

## Break Lab

Break the plan locally, then restore it:

1. Lower `remaining_budget_units` in a passing case below `0.5`.
2. Confirm the simulator routes to `stop_budget_exhausted`.
3. Set `accounting_complete` to `false`.
4. Confirm the simulator routes to `block_incomplete_accounting`.
5. Raise a medium incident full route above `3.5`.
6. Confirm it routes to `request_budget_review`.

## Testing

The validator checks:

- runtime and provider flags remain disabled
- routing scope is AOIS-P only
- budget, confidence, severity, value, and accounting controls exist
- route dimensions are complete
- thresholds are deterministic
- route catalog entries are read-only
- all six decision gates have cases
- live routing prerequisites are listed

## Common Mistakes

- Treating the cheapest route as automatically correct.
- Letting high confidence still trigger unnecessary tools.
- Letting low-severity incidents use high-severity budgets.
- Skipping human review for expensive medium-severity branches.
- Routing when cost accounting is incomplete.
- Forgetting to preserve remaining budget reserve.

## Troubleshooting

If validation fails, inspect the `missing` list.

If simulation fails, compare `decision`, `selected_route`, `expected_decision`,
and `expected_route`.

If a route is unexpectedly stopped, check whether the route fits after the
reserve is preserved:

```text
estimated route cost <= remaining budget - reserve
```

If a route is unexpectedly reviewed, compare its cost to
`expensive_branch_review_cost`.

## Benchmark

The benchmark target is:

- compile succeeds
- validator status `pass`
- simulator status `pass`
- 6 of 6 route cases passing
- no agent runtime
- no routing runtime
- no tool execution
- no provider call
- no billing API call

## Architecture Defense

Budget-aware routing is local and deterministic in this lesson because the goal
is to prove the policy shape.

Live routing would need pricing review, reconciliation, route ownership, human
budget workflow, observability, and primary AOIS separation before enforcement.

## 4-Layer Tool Drill

1. User layer: explain why AOIS chose a cheaper route, review, or stop.
2. App layer: calculate value-to-cost ratios and apply route thresholds.
3. Model layer: avoid unnecessary model/tool steps when evidence is enough.
4. Infra layer: keep runtime, provider, billing, and tool execution disabled.

## 4-Level System Explanation Drill

1. Beginner: AOIS picks the next step based on budget.
2. Practitioner: the router compares severity, evidence, confidence, cost, and value.
3. Operator: expensive or exhausted paths pause before spend happens.
4. Architect: routing turns cost accounting into an agent control plane.

## Failure Story

See [failure-story.md](failure-story.md).

## Mastery Checkpoint

You are ready to move on when you can:

- explain every routing decision gate
- predict the selected route for all six cases
- defend the remaining-budget reserve
- explain why incomplete accounting blocks routing
- explain why high severity can justify a higher-cost route

## Connection Forward

v21 introduces MCP and governed tool registries. Budget-aware routing decides
whether a route should be taken; governed tool registries decide which tools are
available, owned, described, and safe to expose to that route.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.2 Introduction](introduction.md)
- Next: [v20.2 Lab](lab.md)
<!-- AOIS-NAV-END -->
