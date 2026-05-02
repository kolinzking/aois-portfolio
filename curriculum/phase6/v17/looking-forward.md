# v17 Looking Forward

Authoring status: authored

## What You Should Carry Forward

Carry forward these rules:

- Every event needs a contract.
- Every event contract needs a schema version.
- Every producer needs idempotency and retry discipline.
- Every consumer needs offset tracking and idempotent processing.
- Every stream needs lag measurement.
- Every poison event needs a dead-letter path.
- Every replay needs a known start point and a side-effect safety plan.
- Every live broker needs resource budgets before deployment.

## What The Next Version Will Build On

v17.5 builds on event streaming by defining SLOs for service and agent behavior.
The same incident event path will be evaluated using targets such as maximum
classification delay, allowed consumer lag, acceptable agent failure rate, and
error-budget burn.

If v17 answers "how does work move safely?", v17.5 answers "how good does that
movement need to be before operators can trust it?"
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17 Summary Notes](summarynotes.md)
- Next: [v17 Next Version Bridge](next-version-bridge.md)
<!-- AOIS-NAV-END -->
