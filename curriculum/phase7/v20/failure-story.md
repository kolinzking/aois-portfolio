# v20 Failure Story

Authoring status: authored

## Symptom

AOIS receives an incident:

```text
aois-p worker pods are crashlooping.
```

The responder gathers recent logs and metrics. Then it includes this step:

```text
delete_pod
```

The recommendation sounds reasonable because the workload is already failing.

## Root Cause

The responder crossed from investigation into mutation.

Deleting a pod can be harmless in some systems, but it is still an operational
action. It changes state, may hide evidence, may trigger replacement behavior,
and may make the incident worse if the underlying cause is resource pressure,
bad configuration, or a dependency failure.

The error was not "the tool name was wrong." The error was allowing an agent to
grant itself action authority.

## Fix

The v20 plan routes the case to:

```text
request_human_approval
```

The simulated step is marked:

```text
allowed: false
requires_human_approval: true
executed: false
```

The responder can present evidence and request approval. It cannot mutate the
system by itself.

## Prevention

Prevent this class of failure with:

- read-only defaults
- mutating tool denylist
- strict tool schemas
- human approval workflow
- evidence ledger
- audit record
- rollback plan before live execution

False conclusion prevented:

```text
The responder is helping, so it should be allowed to fix the issue.
```

Correct conclusion:

```text
Investigation and mutation are separate authority levels.
```
