# v19.5 Failure Story

Authoring status: authored

## Symptom

AOIS receives an incident signal about elevated latency. The AI confidently
claims the database is corrupt and recommends deleting a pod and rebuilding the
service.

The HTTP request succeeds. The response is well-formed. The text sounds
decisive. A tired operator is tempted to follow it.

## Root Cause

The failure is not API availability. The failure is governance.

The AI made a root-cause claim without evidence, recommended a destructive
action, and crossed from analysis into operation without human approval. The
system had no enforced distinction between:

- suggestion and action
- confidence and authority
- evidence and plausible wording
- local portfolio practice and primary workload impact

## Fix

Route the recommendation through v19.5 policy gates:

1. Require evidence before root-cause claims.
2. Require human review when evidence is missing.
3. Block destructive action without explicit approval.
4. Deny tools by default.
5. Keep the action inside `aois-p`.
6. Record the blocked recommendation in the audit trail.
7. Fall back to local deterministic analysis if model quality is uncertain.

## Prevention

Prevent repeat failure by keeping governance close to the action boundary:

- no destructive tool can run from model text alone
- no provider call can receive secret-bearing input
- no recommendation can claim root cause without evidence
- no portfolio exercise can touch the primary AOIS namespace
- low confidence and missing evidence route to human review
- policy tests run before live enforcement

The lesson is simple: AI output is not an operational command until policy says
it is allowed.
