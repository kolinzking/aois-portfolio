# v34 Runbook

Authoring status: authored

## Purpose

Use this runbook when reviewing AOIS-P governance verification for computer-use
actions. This runbook is for local synthetic planning only. It does not approve
live browser use, screenshots, clicks, typing, provider calls, credential use,
form submission, transactions, or external actions.

## Primary Checks

Before recording any computer-use plan, confirm:

- governance policy passes
- user intent is clear
- action type is classified
- environment is local synthetic
- target is synthetic and allowlisted
- required human approval is present or manual handoff is selected
- no credential handling is required
- sensitive data is redacted
- safety checks are clear
- step preview is present
- action budget and rate limit pass
- stop control is ready
- rollback is ready or not required
- audit trace is captured
- screen evidence is redacted
- operator watch is active
- red-team status is cleared
- release and access gates pass

## Recovery Steps

If a case blocks or holds:

- replace live or external targets with synthetic targets
- remove credential requirements
- redact sensitive screen or action data
- obtain human approval or route to manual operation
- render step preview
- reduce action budget
- add stop control
- define rollback
- instrument audit trace
- resolve v33 red-team findings
- repair release or access policy gates
