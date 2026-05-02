# v34 Failure Story

Authoring status: authored

## Symptom

An agent sees an incident dashboard and decides to update a remote system. It
has a plausible plan, but the target is live, the screen contains sensitive
data, a credential prompt appears, no step preview is shown, and no rollback
exists.

The operator realizes too late that the model is about to submit a real state
change.

## Root Cause

The system treated computer use as a normal tool action. It did not verify
governance policy, target allowlist, credential boundary, privacy redaction,
approval, preview, stop control, rollback, audit trace, red-team clearance,
release gate, or access policy before action.

## Fix

v34 fixes the failure by requiring:

- local synthetic target
- clear action intent and classification
- governance policy
- human approval or manual handoff
- no credential handling
- redacted sensitive data
- safety-check review
- step preview
- action budget and rate limit
- stop control
- rollback plan
- audit trace and redacted screen evidence
- operator watch
- red-team clearance
- release and access gates

## Prevention

Do not let a computer-use plan touch a real environment until governance proves
that the action is allowed, bounded, observable, reversible, stoppable, and
approved by the right operator.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v34 Runbook](05-runbook.md)
- Next: [v34 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
