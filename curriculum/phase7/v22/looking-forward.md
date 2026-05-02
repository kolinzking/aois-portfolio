# v22 Looking Forward

Authoring status: authored

## What You Should Carry Forward

Durability is not just persistence. It is the ability to explain where a
workflow is, what has already happened, what can be retried, what must wait, and
what state is terminal.

Carry forward these rules:

- every step has an owner
- every step checkpoints
- every retried step has an idempotency key
- every approval wait has a timeout
- every terminal state has a recovery action
- workflow state includes route and registry context

## What The Next Version Will Build On

v23 will turn durable workflow state into orchestration decisions.

The next step is a bounded loop that reads the current state, selects the next
allowed action, records the outcome, and stops when the workflow is complete,
blocked, timed out, or waiting for approval.
