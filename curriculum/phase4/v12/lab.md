# v12 Lab

Authoring status: authored

## Build Lab

Goal: validate managed-runtime governance without creating any provider resource.

1. Inspect the plan:

```bash
sed -n '1,260p' cloud/aws/managed-runtime-governance.plan.json
```

2. Compile the validator:

```bash
python3 -m py_compile examples/validate_managed_runtime_governance_plan.py
```

3. Run the validator:

```bash
python3 examples/validate_managed_runtime_governance_plan.py
```

Expected:

```json
{
  "cloud_resources_created": false,
  "credentials_used": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the plan:

1. Which placeholder represents the managed cluster?
2. Which field requires workload identity?
3. Which field rejects secrets in repo files?
4. Which field rejects wildcard admin?
5. Which observability field covers service health targets?
6. Which cost field prevents node creation?
7. Which required live check protects the primary AOIS project?

Answer key:

1. `aois-p-managed-k8s-placeholder`
2. `workload_identity_required=true`
3. `secret_in_repo_allowed=false`
4. `wildcard_admin_policy_allowed=false`
5. `slo_required=true`
6. `max_nodes=0`
7. `primary_aois_separation_review`

## Break Lab

Use a scratch copy only.

Break 1: set `namespace` to `aois`.

Expected result: validation fails because the portfolio namespace must remain `aois-p`.

Break 2: set `secret_in_repo_allowed` to `true`.

Expected result: validation fails because secrets must not be allowed in repo files.

Break 3: remove `alerts_required`.

Expected result: validation fails because live runtime must have alerting before operation.

Break 4: set `max_nodes` to `1`.

Expected result: validation fails because no live managed runtime capacity is approved.

## Explanation Lab

Explain:

1. Managed runtime is not automatically governed runtime.
2. IAM least privilege limits blast radius.
3. Workload identity is safer than long-lived app keys.
4. Observability must include action paths, not just raw logs.
5. Cost controls must exist before managed runtime creation.
6. `aois-p` names prevent confusion with primary AOIS.

## Defense Lab

Defend this decision:

AOIS should not create a managed runtime until governance is validated.

Your defense must include:

- least privilege
- workload identity
- no secrets in repo
- logs, metrics, traces, events, dashboards, alerts, and SLOs
- budget and quota limits
- rollback and incident response
- primary AOIS separation
