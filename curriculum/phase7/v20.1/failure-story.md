# v20.1 Failure Story

Authoring status: authored

## Symptom

AOIS-P gets a medium-severity latency alert. The responder starts with the right
shape: metrics, logs, trace, runbook.

The first pass finds enough evidence to explain the incident. Then the responder
keeps going.

## Root Cause

It asks for another log window because the previous one felt incomplete. It asks
for a wider trace because the incident id had related spans. It asks for a long
runbook excerpt because the short one did not name the exact symptom.

No single step is outrageous. Every step can be defended in isolation.

At the incident level, the investigation has crossed the budget. Worse, one step
was never recorded in the accounting ledger, so the cost total is both high and
untrustworthy.

## Fix

v20.1 prevents this failure by making cost a first-class incident signal:

- every step must be accounted
- every incident must have a total
- repeated tool use is visible
- approval wait is visible
- incomplete accounting blocks trust in the total
- over-budget incidents require review before continuing

## Prevention

The lesson is not that agents should always be cheap. The lesson is that agents
should be economically legible.
