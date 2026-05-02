# v25 Failure Story

Authoring status: authored

## Symptom

An operator approves a remediation action because the incident is urgent. The
agent restarts a worker with broad credentials. The action targets the wrong
environment and there is no rollback plan.

The team now has a production outage caused by an approved action.

## Root Cause

The system treated approval as sufficient execution permission. It did not
require scoped credentials, dry-run staging, sandbox posture, or rollback before
mutation.

## Fix

v25 fixes this by requiring:

- action classification
- deny-by-default policy
- registry checks
- autonomy checks
- credential scope
- sandbox status
- human approval
- guardrail status
- rollback
- dry-run support
- output validation
- audit context

## Prevention

Before enabling any live execution path, prove the local policy:

```bash
python3 examples/validate_safe_execution_boundaries_plan.py
python3 examples/simulate_safe_execution_boundaries.py
```

Then review every new action category for approval, sandbox, filesystem,
network, credential, rollback, dry-run, and output validation requirements.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v25 Runbook](runbook.md)
- Next: [v25 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
