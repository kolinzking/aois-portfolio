# v11 Benchmark

Authoring status: authored

## Measurements

Record:

- validator compile result
- validator status
- namespace
- cloud resources created status
- credentials used status
- live cloud approval status
- max cloud invocations
- repo disk footprint
- memory snapshot

Commands:

```bash
python3 -m py_compile examples/validate_event_workflow_plan.py
python3 examples/validate_event_workflow_plan.py
du -sh .
free -h
```

## Interpretation

A passing benchmark proves the event workflow plan is safe for local learning.

It proves:

- no cloud resource was created
- no credentials were required
- the portfolio namespace is distinct
- message contracts include trace and idempotency controls
- live invocation and spend limits remain zero

It does not prove a provider event workflow is production-ready.

Production readiness requires provider-specific docs review, IAM design, cost guardrails, observability, replay testing, rollback, and explicit approval.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v11 Failure Story](06-failure-story.md)
- Next: [v11 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
