# v25 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether a requested action should
be recorded, staged as a dry run, paused for approval, blocked pending a
boundary, or denied.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm actor role is recorded.
4. Confirm requested action is recorded.
5. Confirm action category is one of the approved categories.
6. Confirm registry decision is recorded.
7. Confirm autonomy mode is recorded.
8. Confirm approval status is recorded.
9. Confirm sandbox status is recorded for execution-capable work.
10. Confirm filesystem scope is bounded.
11. Confirm network policy is explicit.
12. Confirm credential scope is not broad or unknown.
13. Confirm guardrail status is recorded.
14. Confirm idempotency and rollback status are recorded.
15. Confirm dry-run support is recorded.
16. Confirm output validation status is recorded.
17. Confirm trace ID and audit event are present.
18. Confirm no live runtime, sandbox, provider, command, tool, file, network, or cloud flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_safe_execution_boundaries_plan.py
python3 examples/simulate_safe_execution_boundaries.py
```

Decision handling:

- `record_plan_only`: record the policy decision; do not execute.
- `allow_read_only_dry_run`: stage a read-only dry-run plan only.
- `require_sensitive_read_approval`: pause for human approval.
- `require_mutation_approval`: pause for human approval.
- `require_execution_sandbox`: configure an isolated boundary before continuing.
- `block_forbidden_action`: deny immediately.
- `block_registry_denied`: deny and review registry state.
- `block_autonomy_disabled`: deny while autonomy is disabled.
- `block_network_egress`: deny outbound network action.
- `block_credential_scope`: deny until credentials are scoped.
- `block_guardrail_tripwire`: deny and investigate guardrail result.
- `block_output_validation_failure`: deny and investigate failed output validation.
- `block_missing_rollback`: deny until rollback is defined.
- `block_missing_dry_run`: deny until dry-run staging exists.
- `allow_approved_bounded_dry_run`: stage a bounded dry-run plan only.

Escalate to a human operator if:

- the action category is disputed
- approval and registry state disagree
- a team requests broad credentials
- network egress is requested
- sandbox boundaries are unclear
- rollback cannot be proven
- dry-run output conflicts with expected state
