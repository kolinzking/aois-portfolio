# v19 Failure Story

Authoring status: authored

## Symptom

Someone runs a memory stress command on the shared server to "test resilience."
The primary AOIS workload starts showing memory pressure and the server becomes
less stable.

## Root Cause

The activity was not chaos engineering. It had no steady-state check, no
hypothesis, no blast radius, no SLO budget review, no primary-project exclusion,
no abort condition, and no rollback plan.

## Fix

Stop the experiment, treat the memory pressure as an operational risk, restore
server headroom, and replace the live stress attempt with a tabletop
experiment. Define steady state, hypothesis, blast radius, abort condition,
rollback, owner, observer, and post-review before any live chaos is considered.

## Prevention

Prevent recurrence by requiring:

- primary AOIS exclusion
- SLO budget review
- resource headroom review
- blast-radius approval
- abort conditions
- rollback plan
- incident commander or game-day owner
- post-game-day review

Chaos without controls is just avoidable failure.
