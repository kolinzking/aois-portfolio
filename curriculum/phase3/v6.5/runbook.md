# v6.5 Runbook

Authoring status: authored

## Purpose

Use this runbook when workload identity validation fails or RBAC/network policy changes are being considered.

## Primary Checks

Validate:

```bash
python3 examples/validate_k8s_identity_plan.py
```

Inspect:

```bash
sed -n '1,160p' k8s/aois-p/service-account.yaml
sed -n '1,160p' k8s/aois-p/role.yaml
sed -n '1,200p' k8s/aois-p/network-policy.yaml
```

## Recovery Steps

If validation fails:

- read `missing`
- restore the referenced manifest field
- rerun the validator

If someone wants to apply:

- stop
- confirm namespace `aois-p`
- confirm RBAC scope
- confirm token automount behavior
- confirm NetworkPolicy impact
- get explicit approval
