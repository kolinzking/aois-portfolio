# v20.2 Failure Story

Authoring status: authored

## Symptom

AOIS-P has a medium-severity incident with missing evidence. The responder has
three candidate routes: a cheap no-tool summary, a bounded read-only pass, and a
full trace-heavy investigation.

## Root Cause

The system chooses the full investigation because it has the highest expected
value. It does not check whether the branch is expensive for a medium-severity
incident, and it does not preserve a budget reserve.

The result is not a bad answer. The result is an answer that spent too much too
early.

## Fix

v20.2 fixes this by routing before spend:

- complete high-confidence evidence can use a small no-tool route
- partial evidence can use one bounded read-only route
- expensive medium-severity branches pause for budget review
- exhausted budget stops before spending
- high severity can justify a full route when the value-to-cost ratio is strong
- incomplete accounting blocks routing

## Prevention

Treat routing as part of the agent control plane. A route is not selected because
it is possible; it is selected because severity, evidence, confidence, value,
cost, and remaining budget agree.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.2 Runbook](05-runbook.md)
- Next: [v20.2 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
