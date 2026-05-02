# v11 Runbook

Authoring status: authored

## Purpose

This runbook restores the `v11` event workflow plan to a safe no-cloud state.

Safe state means:

- namespace is `aois-p`
- no cloud resource was created
- no credentials were used
- live cloud approval is false
- live invocation limits are zero
- retry, DLQ, idempotency, trace, cost, observability, IAM, and rollback controls exist

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_event_workflow_plan.py
python3 examples/validate_event_workflow_plan.py
```

Inspect:

```bash
sed -n '1,260p' cloud/aws/event-workflow.plan.json
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
3. Restore all workflow names to the `aois-p-` prefix.
4. Restore `cloud_resources_created` to `false`.
5. Restore `credentials_used` to `false`.
6. Restore `approved_for_live_cloud` to `false`.
7. Restore `trace_id` and `idempotency_key`.
8. Restore all required controls to `true`.
9. Restore `max_cloud_invocations`, `max_concurrency`, and `max_spend_usd` to `0`.
10. Rerun validation.

If live event workflow work is requested:

1. Stop this lesson path.
2. Review official provider documentation.
3. Define IAM least privilege.
4. Define credentials and secret storage.
5. Define budget and max invocation guardrails.
6. Define event schema and payload limits.
7. Define DLQ replay and rollback.
8. Get explicit approval before creating cloud resources.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v11 Lab](04-lab.md)
- Next: [v11 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
