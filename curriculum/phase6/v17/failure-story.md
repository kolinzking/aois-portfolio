# v17 Failure Story

Authoring status: authored

## Symptom

AOIS incident automation appears stuck. New incident events are still being
written, but the recommendation agent is no longer producing remediation
suggestions. The dashboard shows consumer lag increasing.

## Root Cause

A malformed event entered the stream after an agent workflow changed its
payload shape without updating the event contract. The consumer retries the
same event repeatedly and never advances its offset. Because there is no
dead-letter policy, one poison event blocks every event behind it.

## Fix

Move the malformed event to a dead-letter stream, fix or reject the bad schema,
and replay from the last safe offset. The consumer must process events
idempotently because replay can re-read events that already produced side
effects.

## Prevention

Prevent the failure by requiring:

- Schema validation before publish.
- Versioned event contracts.
- Consumer offset tracking.
- Lag measurement.
- Dead-letter routing for poison events.
- Replay runbooks.
- Backpressure rules when consumers cannot keep up.

In v17, the validator enforces these controls before any broker is allowed.
