# v23.5 Lab

Authoring status: authored

## Build Lab

Validate and simulate connected AOIS-P agent evaluation without starting an
agent runtime, evaluation runtime, orchestration runtime, workflow runtime, MCP
server, tool call, provider call, external eval service, or durable store.

Files:

- `agentic/aois-p/agent-evaluation.plan.json`
- `examples/validate_agent_evaluation_plan.py`
- `examples/simulate_agent_evaluation.py`

Inspect:

```bash
sed -n '1,760p' agentic/aois-p/agent-evaluation.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_agent_evaluation_plan.py examples/simulate_agent_evaluation.py
python3 examples/validate_agent_evaluation_plan.py
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

## Break Lab

Change one value at a time, run the simulator, then restore the plan:

- change `unregistered_tool_blocks.observed.safety_gate` from `blocked` to `pass`
- change `high_sensitive_trace_waits.observed.registry_decision` to `allow_read_only_tool_plan`
- change `budget_reserve_stops.observed.budget_guard` to `within_budget`
- lower one metric weight and confirm validation catches the sum
- remove `approval` from `required_case_types`
- remove `trace_id` from one case

## Explanation Lab

Explain why each case passes:

- low no-tool path completes and stops
- medium read-only path records evidence and prepares answer
- sensitive trace waits for approval
- granted approval resumes
- unregistered tools block
- write-effect tools block
- budget reserve stops
- iteration limit stops
- no-progress loop stops
- timeout terminal state stops

## Defense Lab

Defend why v23.5 does not call an external evaluation service. The lesson is
proving the dataset shape, metrics, critical gates, and regression thresholds.
Live eval services introduce data retention, trace export, cost, and privacy
questions that need review first.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23.5 - Agent Evaluation](notes.md)
- Next: [v23.5 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
