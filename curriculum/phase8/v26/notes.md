# v26 - Dashboard And Real-Time Visibility

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no API server,
no frontend runtime, no dashboard deployment, no browser, no WebSocket server,
no SSE stream, no agent runtime, no execution runtime, no tool execution, no
command execution, no file write during validation, no network call, no provider
call, no external network during validation, no persistent storage

## What This Builds

This version builds a product-surface visibility contract and simulation:

- `product/aois-p/dashboard-visibility.plan.json`
- `examples/validate_dashboard_visibility_plan.py`
- `examples/simulate_dashboard_visibility.py`

It teaches:

- dashboard panel contracts
- event-driven operator state
- incident overview design
- trace timeline visibility
- route and registry visibility
- workflow and orchestration visibility
- autonomy and agent visibility
- approval queue visibility
- budget and execution-boundary visibility
- stale data, connection loss, empty state, redaction, and accessibility gates

## Why This Exists

Phase 7 built the governed operating model. That model is not useful to humans
until it is visible.

Operators need to see why AOIS-P made a decision, what state is current, which
approval is waiting, whether a trace is stale, whether a budget reserve is
low, whether an agent handoff happened, and why an execution boundary blocked
an action.

The central dashboard question is:

```text
Given the latest AOIS-P event, event freshness, connection state, redaction
state, accessibility state, budget state, and incident scope, which dashboard
panel should be active and what should the operator do next?
```

v26 answers that question locally. It does not build or start a React app.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state`

v26 consumes Phase 7 state:

- route decisions
- registry decisions
- workflow checkpoints
- orchestration decisions
- evaluation scores
- autonomy mode
- agent handoffs
- approvals
- budget status
- execution-boundary decisions

The output is a dashboard decision: active panel, status badge, and operator
action.

## Learning Goals

By the end of this version you should be able to:

- define the panels an AOIS operator needs
- map backend events to dashboard state
- explain why UI state should derive from event state
- distinguish live streaming from local event replay
- design stale data and connection-loss indicators
- block sensitive payload rendering until redaction passes
- block release readiness when accessibility checks fail
- validate and simulate dashboard visibility locally

## Prerequisites

You should have completed:

- Phase 6 observability and incident-response lessons
- `v20` through `v25` in Phase 7
- the FastAPI service shape from Phase 0

Required checks:

```bash
python3 -m py_compile examples/validate_dashboard_visibility_plan.py examples/simulate_dashboard_visibility.py
python3 examples/validate_dashboard_visibility_plan.py
python3 examples/simulate_dashboard_visibility.py
```

## Core Concepts

## Product Surface

The product surface is the operator's view of AOIS. It is not a decorative
layer. It changes how the system is operated because it decides what state is
visible, what looks urgent, and what action the operator sees next.

## Panel Contract

Each panel has:

- owner
- source phase
- primary fields
- update events
- empty state
- stale threshold
- accessibility label

This keeps dashboard design tied to operational state instead of generic cards.

## Event Model

The dashboard contract uses ordered events. Every event needs an ID, sequence
number, incident ID, trace ID, event type, source phase, summary, redaction
status, and audit event.

v26 simulates event replay only. It does not start WebSockets or SSE.

## Freshness

Dashboard state can be wrong even when it looks polished. v26 requires stale
state indicators when an event is older than the panel freshness budget.

## Redaction Gate

Sensitive payloads must not render unless redaction passed. The simulator
blocks unredacted sensitive payloads before it chooses a normal panel state.

## Accessibility Gate

Operator dashboards are repeated-use tools. v26 treats accessibility as a
release gate, not a cosmetic pass.

## Build

Inspect:

```bash
sed -n '1,900p' product/aois-p/dashboard-visibility.plan.json
sed -n '1,380p' examples/validate_dashboard_visibility_plan.py
sed -n '1,260p' examples/simulate_dashboard_visibility.py
```

Compile:

```bash
python3 -m py_compile examples/validate_dashboard_visibility_plan.py examples/simulate_dashboard_visibility.py
```

Validate:

```bash
python3 examples/validate_dashboard_visibility_plan.py
```

Simulate:

```bash
python3 examples/simulate_dashboard_visibility.py
```

Expected:

```json
{
  "passed_cases": 13,
  "score": 1.0,
  "status": "pass",
  "total_cases": 13
}
```

## Ops Lab

1. Open the dashboard visibility plan.
2. Find `dashboard_panels`.
3. Confirm each panel has source phase, owner, fields, events, empty state, stale threshold, and accessibility label.
4. Find `event_model`.
5. Confirm ordering, dedupe, required fields, and supported event types.
6. Find `visibility_cases`.
7. Confirm each decision gate has a case.
8. Run the validator.
9. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Remove `execution_boundaries` from `dashboard_panels`.
2. Confirm validation fails.
3. Restore the panel.
4. Change `unredacted_payload_blocked.redaction_status` to `redacted`.
5. Confirm simulation no longer blocks rendering.
6. Restore the value.
7. Change `stale_data_warning.event_age_seconds` to `5`.
8. Confirm simulation no longer shows the stale warning.
9. Restore the value.
10. Remove `keyboard_navigation_test` from live dashboard checks.
11. Confirm validation fails.
12. Restore the check.

## Testing

The validator checks:

- no API server, frontend runtime, stream, browser, provider, network, or live dashboard flags are enabled
- AOIS-P scope and primary AOIS separation are explicit
- source notes are recorded
- required dashboard controls exist
- all eight panels are defined
- event model has ordering and dedupe keys
- required event fields and event types exist
- all thirteen dashboard decisions have cases
- live dashboard prerequisites are listed

## Common Mistakes

- Treating a dashboard as a set of pretty cards.
- Showing stale state without warning.
- Hiding trace, approval, budget, or execution-boundary state behind details.
- Rendering sensitive data before redaction passes.
- Treating accessibility as a late polish task.
- Confusing local event replay with a live WebSocket or SSE stream.
- Making every panel look equally urgent.
- Forgetting that operators need a next action, not only raw state.

## Troubleshooting

If validation fails:

- inspect the `missing` list
- confirm every runtime flag is false
- confirm all panels exist
- confirm all event fields exist
- confirm every decision has a case
- confirm live dashboard checks include accessibility and redaction review

If simulation fails:

- compare `decision` to `expected_decision`
- check the priority order in `_decide`
- confirm redaction and accessibility blocks run before normal panel routing
- confirm stale data is checked before event-specific panel decisions
- confirm the latest event maps to the expected panel

## Benchmark

Pass criteria:

- validator status is `pass`
- simulator status is `pass`
- simulator score is `1.0`
- all thirteen visibility cases pass
- no API, frontend, stream, browser, provider, network, or live dashboard flag is enabled

## Architecture Defense

Defend this design:

AOIS-P does not start a React app in v26 because the first product-surface
milestone is a stable visibility contract. The dashboard should reflect the
operating model built in Phase 7 before implementation choices like component
libraries, live transport, and layout are introduced.

## 4-Layer Tool Drill

Use the AOIS dashboard lens:

1. Product layer: what does the operator need to know right now?
2. State layer: which incident, trace, event, panel, and badge represent that state?
3. Runtime layer: is this local replay, SSE, WebSocket, or API polling?
4. Failure layer: what happens when data is stale, disconnected, unredacted, inaccessible, or empty?

## 4-Level System Explanation Drill

Explain v26 at four levels:

1. Beginner: the dashboard chooses which AOIS state an operator should see.
2. Operator: incidents, traces, approvals, budget, agents, and execution boundaries must be visible together.
3. Engineer: event replay maps latest event and safety gates to active panel, badge, and operator action.
4. Architect: a product surface is an operational control plane, not a presentation afterthought.

## Failure Story

An execution boundary blocks a risky action, but the dashboard only shows the
incident summary. The operator assumes the system is idle and opens a separate
manual change. The original boundary decision was correct, but it was hidden.

v26 prevents this by making execution-boundary decisions a first-class panel
and by mapping the latest boundary event to a visible status badge and operator
action.

## Mastery Checkpoint

You have mastered v26 when you can:

- list the eight dashboard panels
- explain why stale state needs a visible warning
- explain why redaction and accessibility are release gates
- add a new event type and dashboard case
- defend why v26 uses local event replay instead of live streaming
- describe how v27 will add identity and policy-aware access

## Connection Forward

v27 adds auth, tenancy, permissions, and policy-aware user access.

After AOIS-P can show operational state, it must decide who is allowed to see
which incidents, traces, approvals, budget records, agent state, and execution
boundary decisions.

## Source Notes

Checked 2026-05-02.

- OpenTelemetry trace concepts documentation: used for trace, span, event, and observability vocabulary.
- OpenAI API tools and evals documentation: used for current agent/tool/evaluation terminology that appears in dashboard state.
- v26 is a local product-surface state contract. It does not start a frontend, SSE stream, WebSocket, collector, provider call, or dashboard runtime.
