# v12 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v12` managed-runtime governance plan to a safe no-cloud state.

Safe state means:

- namespace is `aois-p`
- no cloud resource was created
- no credentials were used
- live cloud approval is false
- wildcard admin is disallowed
- static keys are disallowed
- secrets in repo are disallowed
- cost limits remain zero
- observability and operational controls are required

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_managed_runtime_governance_plan.py
python3 examples/validate_managed_runtime_governance_plan.py
```

Inspect:

```bash
sed -n '1,260p' cloud/aws/managed-runtime-governance.plan.json
```

Required result:

- `status` is `pass`
- `cloud_resources_created` is `false`
- `credentials_used` is `false`
- `namespace` is `aois-p`

## Recovery Steps

If validation fails:

1. Read the `missing` list.
2. Restore `namespace` to `aois-p`.
3. Restore every managed runtime placeholder to the `aois-p-` prefix.
4. Restore `cloud_resources_created` to `false`.
5. Restore `credentials_used` to `false`.
6. Restore `approved_for_live_cloud` to `false`.
7. Restore least privilege and workload identity to `true`.
8. Restore wildcard admin, static keys, and secrets in repo to `false`.
9. Restore observability controls to `true`.
10. Restore cost limits to zero.
11. Restore operational controls and required live checks.
12. Rerun validation.

If live managed-runtime work is requested:

1. Stop the lesson path.
2. Review official provider documentation.
3. Define IAM least privilege.
4. Define workload identity.
5. Define credential and secret handling.
6. Define budget, quotas, and cost alarms.
7. Define logs, metrics, traces, events, dashboards, alerts, and SLOs.
8. Define capacity, backup/restore, rollback, and incident response.
9. Verify primary AOIS separation.
10. Get explicit approval before creating resources.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v12 Lab](lab.md)
- Next: [v12 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
