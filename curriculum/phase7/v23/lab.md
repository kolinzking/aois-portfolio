# v23 Lab

Authoring status: authored

## Build Lab

Validate and simulate stateful AOIS-P orchestration loops without starting an
agent runtime, orchestration runtime, workflow runtime, MCP server, tool call,
provider call, or durable store.

Files:

- `agentic/aois-p/stateful-orchestration.plan.json`
- `examples/validate_stateful_orchestration_plan.py`
- `examples/simulate_stateful_orchestration.py`

Inspect:

```bash
sed -n '1,720p' agentic/aois-p/stateful-orchestration.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_stateful_orchestration_plan.py examples/simulate_stateful_orchestration.py
python3 examples/validate_stateful_orchestration_plan.py
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

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove `stop_no_progress` from `decision_precedence`
- move `wait_for_approval` before `stop_registry_block`
- set `max_iterations` to `10`
- set `min_budget_reserve_units` to `0`
- set an action's `executes_tool` to `true`
- make `no_progress_stops.previous_state_hash` differ from `state_hash`

## Explanation Lab

Explain why each case chooses its decision:

- terminal states stop immediately
- missing approval waits
- granted approval resumes
- read-only registry checks plan evidence
- recorded evidence prepares an answer
- prepared answers close workflows
- registry blocks stop
- budget reserve stops
- iteration limit stops
- unchanged state hash stops

## Defense Lab

Defend why v23 does not start an orchestration framework. Orchestration is where
autonomy loops can bypass policy. AOIS-P first proves the ordered decision
rules and loop guards locally before introducing a live runtime.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23 - Stateful Orchestration Loops](notes.md)
- Next: [v23 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
