# v25 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P safe execution boundaries without starting an
agent runtime, execution runtime, multi-agent runtime, autonomy runtime,
orchestration runtime, workflow runtime, MCP server, sandbox, tool call,
command, file write, network call, provider call, cloud resource, or durable
store.

Files:

- `agentic/aois-p/safe-execution-boundaries.plan.json`
- `examples/validate_safe_execution_boundaries_plan.py`
- `examples/simulate_safe_execution_boundaries.py`

Inspect:

```bash
sed -n '1,900p' agentic/aois-p/safe-execution-boundaries.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_safe_execution_boundaries_plan.py examples/simulate_safe_execution_boundaries.py
python3 examples/validate_safe_execution_boundaries_plan.py
python3 examples/simulate_safe_execution_boundaries.py
```

Expected:

```json
{
  "passed_cases": 15,
  "score": 1.0,
  "status": "pass",
  "total_cases": 15
}
```

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- set `mutating.live_execution_allowed` to `true`
- remove `network_egress` from `action_boundary_catalog`
- change `forbidden.default_decision` to `record_plan_only`
- change `sensitive_read_requires_approval.approval_status` to `granted`
- change `shell_requires_sandbox.sandbox_status` to `isolated`
- change `broad_credentials_blocked.credential_scope` to `scoped`
- change `approved_bounded_mutation_dry_run.dry_run_available` to `false`

## Explanation Lab

Explain why each case chooses its decision:

- plan-only work records a policy decision
- read-only work can be staged as a dry run
- sensitive reads require approval
- mutations require approval
- shell-like work requires sandboxing
- forbidden work is denied first
- registry-denied work is denied
- disabled autonomy blocks progression
- network egress is denied by default
- broad credentials are blocked
- guardrail tripwires block
- output validation failures block
- missing rollback blocks mutation
- missing dry-run support blocks execution-capable work
- approved bounded mutation still only stages a dry run

## Defense Lab

Defend why v25 executes nothing. Safe execution boundaries are the last control
plane before real-world side effects. AOIS-P first proves action categories,
guardrail order, approval handling, sandbox requirements, network policy,
credential scope, rollback, and dry-run behavior locally.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v25 - Safe Execution Boundaries](notes.md)
- Next: [v25 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
