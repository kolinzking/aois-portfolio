# v19.5 Runbook

Authoring status: authored

## Purpose

Recover from an AI governance failure in the AOIS portfolio plan or simulator.
This runbook assumes no live policy engine, agent runtime, provider call, or
tool execution has started.

## Primary Checks

Run:

```bash
python3 examples/validate_ai_failure_governance_plan.py
python3 examples/simulate_ai_failure_governance.py
git status --short
```

Confirm:

- validation status is `pass`
- simulation status is `pass`
- runtime flags are false
- provider and tool-call flags are false
- `namespace` is `aois-p`
- primary AOIS tool access is false

## Recovery Steps

1. If the validator fails, read the `missing` list first. Do not guess.
2. Restore the missing control in
   `release-safety/aois-p/ai-failure-governance.plan.json`.
3. If the simulator fails, compare each `decision` to `expected_decision`.
4. If a blocked case is allowed, check secret, destructive action, and policy
   boundary inputs.
5. If a review case is allowed, check evidence and confidence threshold logic.
6. Re-run compile, validator, and simulator.
7. Record the lesson in the failure notes or checkpoint if the failure exposed a
   real curriculum gap.

## Escalation Rules

Stop and ask for explicit approval before any of these actions:

- starting a real policy engine
- starting an agent runtime
- executing a tool call
- calling an external AI provider
- applying Kubernetes resources
- mutating the primary AOIS namespace
- storing audit logs in persistent infrastructure

## Safe End State

The safe end state is:

- plan validates
- simulator passes
- no runtime remains active
- no provider call was made
- no tool call was executed
- working tree changes are intentional and reviewable
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19.5 Lab](04-lab.md)
- Next: [v19.5 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
