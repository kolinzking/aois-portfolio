# v28 Failure Story

Authoring status: authored

## Symptom

AOIS-P ships a dashboard and model behavior update after unit tests pass. The
release degrades incident handling for several tenants. Operators cannot tell
which artifact was deployed, whether it was signed, whether the signature was
verified, or which feature flag enabled the new behavior.

## Root Cause

The team treated a passing test job as release safety. The workflow had broad
write permissions, the artifact had no digest-bound evidence, build provenance
was missing, signature verification was skipped, environment approval was
informal, rollout health was not gated, rollback was undefined, and model
behavior shipped without a guarded feature flag.

## Fix

v28 fixes the failure with delivery release controls:

- source and branch review gate
- least-privilege workflow gate
- dependency, test, policy, and security gates
- artifact digest and provenance gates
- signature and verification gates
- environment approval gate
- rollout health and rollback gates
- staged model rollout
- guarded feature flags

## Prevention

Before live delivery:

- review workflow YAML and permissions
- configure branch protection
- configure dependency review
- review the test matrix
- review policy regression coverage
- review security scans
- review provenance and signature identity
- verify signatures before release
- require environment approval
- rehearse rollback
- review model rollout and feature-flag plans
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v28 Runbook](runbook.md)
- Next: [v28 Benchmark](benchmark.md)
<!-- AOIS-NAV-END -->
