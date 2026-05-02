# v12 Benchmark

Authoring status: authored

## Measurements

Record:

- validator compile result
- validator status
- namespace
- cloud resources created status
- credentials used status
- live cloud approval status
- wildcard admin status
- static key status
- max spend
- max clusters
- max nodes
- repo disk footprint
- memory snapshot

Commands:

```bash
python3 -m py_compile examples/validate_managed_runtime_governance_plan.py
python3 examples/validate_managed_runtime_governance_plan.py
du -sh .
free -h
```

## Interpretation

A passing benchmark proves the governance plan is safe for local learning.

It proves:

- no managed runtime was created
- no credentials were used
- names remain `aois-p`
- IAM rejects broad access and static keys
- observability and operational controls are required
- cloud capacity and spend remain zero

It does not prove provider-specific production readiness.

Production readiness requires official provider docs review, account-specific IAM design, network review, cost review, observability buildout, rollback rehearsal, and explicit approval.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v12 Failure Story](failure-story.md)
- Next: [v12 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
