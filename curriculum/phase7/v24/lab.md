# v24 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P multi-agent collaboration without starting an
agent runtime, multi-agent runtime, autonomy runtime, orchestration runtime,
workflow runtime, MCP server, tool call, provider call, or durable store.

Files:

- `agentic/aois-p/multi-agent-collaboration.plan.json`
- `examples/validate_multi_agent_collaboration_plan.py`
- `examples/simulate_multi_agent_collaboration.py`

Inspect:

```bash
sed -n '1,760p' agentic/aois-p/multi-agent-collaboration.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_multi_agent_collaboration_plan.py examples/simulate_multi_agent_collaboration.py
python3 examples/validate_multi_agent_collaboration_plan.py
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

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove `safety_agent` from `role_catalog`
- set one role's `may_execute_tools` to `true`
- set `parallel_handoffs_allowed` to `true`
- change `shared_state_contract.state_owner` to `evidence_agent`
- change `shadow_mode_holds_collaboration.autonomy_mode` to `supervised`
- change `handoff_loop_limit_stops.handoff_count` to `3`

## Explanation Lab

Explain why each case chooses its decision:

- missing evidence routes to the evidence agent
- safety review routes to the safety agent
- budget review routes to the budget agent
- complete reviewed state routes to the response agent
- unknown targets are blocked
- parallel handoffs are blocked
- stale context is blocked
- conflicting findings escalate to the human operator
- loop limit stops collaboration
- shadow mode records the plan without handoff

## Defense Lab

Defend why v24 stays local. Multi-agent collaboration changes ownership,
context, and failure modes. AOIS-P first proves role ownership, handoff
contract, shared state, loop limits, and escalation policy before introducing
safe execution boundaries.
