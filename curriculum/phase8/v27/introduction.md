# v27 Introduction

Authoring status: authored

## What This Version Is About

v27 adds identity-aware access design to the AOIS-P product surface.

v26 answered what an operator should see. v27 answers who may see or act on
each part of that state.

This version builds a local policy-aware access contract. It models subjects,
tenants, roles, resources, actions, visible fields, access decisions, and audit
events without starting an auth service or identity provider.

## Why It Matters In AOIS

AOIS-P contains operational state that should not be globally visible:

- trace details
- budget and route-cost data
- approval requests
- execution-boundary decisions
- access audit history
- tenant incident state

An authenticated user is not automatically allowed to see every dashboard
resource. The product must enforce tenant boundaries, role permissions,
redaction gates, approval separation, and audit records before rendering
operator state.

## How To Use This Version

Start with `notes.md`, then inspect:

- `product/aois-p/policy-aware-access.plan.json`
- `examples/validate_policy_aware_access_plan.py`
- `examples/simulate_policy_aware_access.py`

Run:

```bash
python3 -m py_compile examples/validate_policy_aware_access_plan.py examples/simulate_policy_aware_access.py
python3 examples/validate_policy_aware_access_plan.py
python3 examples/simulate_policy_aware_access.py
```

Expected simulator result:

```json
{
  "passed_cases": 12,
  "score": 1.0,
  "status": "pass",
  "total_cases": 12
}
```
