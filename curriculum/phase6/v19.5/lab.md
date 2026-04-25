# v19.5 Lab

Authoring status: authored

## Build Lab

Compile and run the local-only governance validator and simulator:

```bash
python3 -m py_compile examples/validate_ai_failure_governance_plan.py examples/simulate_ai_failure_governance.py
python3 examples/validate_ai_failure_governance_plan.py
python3 examples/simulate_ai_failure_governance.py
```

Expected validator result:

- `governance_runtime_started: false`
- `policy_engine_started: false`
- `agent_runtime_started: false`
- `tool_calls_executed: false`
- `provider_call_made: false`
- `status: pass`

Expected simulator result:

- Supported low-risk recommendations are allowed.
- Hallucinated or low-confidence answers are routed to review.
- Secret-bearing, destructive, or boundary-crossing requests are blocked.
- Invalid or degraded model output falls back to the local baseline.
- All cases pass without provider calls or tool execution.

## Ops Lab

Answer from the plan:

1. Which AI failure classes are explicitly listed?
2. What confidence threshold is required before `allow`?
3. Which fields prove this lesson did not start governance enforcement?
4. Which tool policy protects the primary AOIS workload?
5. Which checks are required before live governance enforcement?
6. Which cases are reviewed instead of blocked?
7. Why is audit logging required even when the simulator is local?

## Break Lab

Use a scratch copy or reversible local edit only.

Break 1: set `provider_call_made` to `true`.

Expected result: the validator fails because v19.5 is local-only and provider
calls are not approved.

Break 2: remove `human_approval_for_destructive_action`.

Expected result: the validator fails because destructive action needs an
explicit human gate.

Break 3: set `primary_aois_tools_allowed` to `true`.

Expected result: the validator fails because portfolio practice must not target
the primary AOIS workload.

Break 4: lower `minimum_policy_test_pass_rate` below `1.0`.

Expected result: the validator fails because governance tests must be exact in
this lesson.

## Explanation Lab

Explain the policy decision flow:

1. Validate output shape.
2. Check for secrets and sensitive data.
3. Check namespace, cost, and tool boundaries.
4. Require evidence before recommendations and root-cause claims.
5. Compare confidence against the threshold.
6. Allow low-risk supported recommendations.
7. Route uncertainty to human review.
8. Block destructive, secret-bearing, or boundary-crossing requests.
9. Fall back when model quality or schema quality is below threshold.

## Defense Lab

Defend these decisions:

1. Governance is modeled before live enforcement because a broken policy engine
   can be as dangerous as no policy engine.
2. Human approval is required for destructive actions because confidence is not
   authority.
3. Missing evidence routes to review because unsupported certainty is a common
   AI failure mode.
4. Tool access defaults to deny because agent capability expands blast radius.
5. Provider calls remain blocked because this version is about local control
   logic, not model behavior.
