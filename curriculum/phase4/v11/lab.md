# v11 Lab

Authoring status: authored

## Build Lab

Goal: validate an event-driven workflow plan without creating any cloud resource.

1. Inspect the plan:

```bash
sed -n '1,260p' cloud/aws/event-workflow.plan.json
```

2. Compile the validator:

```bash
python3 -m py_compile examples/validate_event_workflow_plan.py
```

3. Run the validator:

```bash
python3 examples/validate_event_workflow_plan.py
```

Expected result:

```json
{
  "cloud_resources_created": false,
  "credentials_used": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Use the plan to answer:

1. What is the workflow name?
2. Which field contains the queue placeholder?
3. Which field contains the DLQ placeholder?
4. Which message field supports deduplication?
5. Which live limit prevents cloud execution?
6. Which operational check covers IAM?

Answer key:

1. `aois-p-ai-incident-event-flow`
2. `workflow.queue`
3. `workflow.dead_letter_queue`
4. `idempotency_key`
5. `max_cloud_invocations=0`
6. `iam_least_privilege_review`

## Break Lab

Use a scratch copy only.

Break 1: set `namespace` to `aois`.

Expected result: validation fails because portfolio resources must use `aois-p`.

Break 2: remove `trace_id`.

Expected result: validation fails because distributed debugging needs trace propagation.

Break 3: set `limits.max_cloud_invocations` to `1`.

Expected result: validation fails because no live cloud invocation is approved.

## Explanation Lab

Explain:

1. Why a queue is not enough without idempotency.
2. Why a DLQ is not useful without a replay runbook.
3. Why event payloads should stay small.
4. Why trace IDs must survive ingress, queue, worker, and result sink.
5. Why `aois-p` naming matters on a shared server/provider portfolio.

## Defense Lab

Defend this decision:

AOIS should plan event-driven workflows locally before creating cloud queues or functions.

Your defense must include:

- cost control
- IAM least privilege
- idempotency
- DLQ replay
- observability
- rollback
- separation from primary AOIS resources
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v11 - Event-Driven Workflow Planning Without Cloud Calls](notes.md)
- Next: [v11 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
