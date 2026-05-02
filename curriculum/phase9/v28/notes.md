# v28 - Delivery Pipeline And Release Controls

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no CI runtime,
no workflow run, no build, no test runner, no container build, no image push, no
signing action, no signature verification action, no deployment, no Kubernetes
apply, no rollout, no traffic shift, no feature-flag service call, no model
endpoint change, no network call, no provider call, no persistent storage

## What This Builds

This version builds a local delivery and release-control contract:

- `release-safety/aois-p/delivery-release-controls.plan.json`
- `examples/validate_delivery_release_controls_plan.py`
- `examples/simulate_delivery_release_controls.py`

It teaches:

- CI/CD pipeline stages
- workflow permissions
- source and branch gates
- tests in delivery
- policy regression gates
- artifact digest and provenance
- image signing and signature verification
- environment approvals
- rollout health gates
- rollback readiness
- model rollout control
- feature-flagged AI releases

## Why This Exists

Phase 8 made AOIS-P visible and access-controlled. That is not enough if unsafe
changes can ship around the controls.

The central release question is:

```text
Given source review, workflow permissions, dependency review, tests, policy
checks, security scans, artifact identity, provenance, signature evidence,
environment approval, rollout health, rollback readiness, model rollout state,
and feature-flag state, should AOIS-P promote, block, or hold the release?
```

v28 answers that question locally. It does not create a GitHub Actions
workflow, build an image, sign anything, deploy to Kubernetes, shift traffic,
or mutate feature flags.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state -> scope access -> release changes safely`

v28 consumes Phase 8 outcomes:

- dashboard visibility regressions must stay green
- policy-aware access regressions must stay green
- AOIS-P remains separate from primary AOIS
- release evidence must be reviewable before promotion

The output is a release decision: promote, block, or hold.

## Learning Goals

By the end of this version you should be able to:

- explain what a delivery pipeline adds beyond local tests
- distinguish a build artifact from release evidence
- require least-privilege workflow permissions
- block unreviewed branches
- block failed tests, policy regressions, and security scans
- require artifact digest, provenance, signature, and verification evidence
- require environment approval before rollout
- hold rollouts on degraded health
- require rollback readiness
- treat model rollout and feature flags as release controls
- validate and simulate release decisions locally

## Prerequisites

You should have completed:

- Phase 7 governance and execution-boundary lessons
- Phase 8 dashboard visibility and policy-aware access lessons

Required checks:

```bash
python3 -m py_compile examples/validate_delivery_release_controls_plan.py examples/simulate_delivery_release_controls.py
python3 examples/validate_delivery_release_controls_plan.py
python3 examples/simulate_delivery_release_controls.py
```

## Core Concepts

## Delivery Pipeline

A delivery pipeline turns a change into release evidence. v28 models five
stages:

- source control
- build and test
- package and attest
- release gate
- rollout control

Every stage blocks on failure.

## Workflow Permissions

The plan requires least-privilege workflow permissions. A workflow that can
write everything can become a release bypass even when the tests are correct.

## Tests In Delivery

v28 treats unit, integration, dashboard visibility, and policy-aware access
regressions as release gates. Passing locally is not enough; delivery must
prove the same controls before promotion.

## Artifact Identity

The release candidate needs a digest. Without an artifact digest, the team
cannot prove which thing was tested, signed, approved, or deployed.

## Provenance And Signature Evidence

Provenance describes how the artifact was built. A signature ties the artifact
to an expected signing identity. Verification proves the signature evidence
was checked before release.

v28 models these controls but does not run a real signing tool.

## Environment Approval

Environment approval is the human gate for production-like release. It should
not be replaced by a passing build.

## Rollout Health

A release can pass every pre-release gate and still fail during rollout. v28
holds rollout when health is degraded or unknown.

## Rollback Readiness

Rollback is a release prerequisite, not an emergency improvisation. v28 blocks
release when rollback target or rollback plan is missing.

## Model Rollout Control

AI behavior changes can be riskier than normal code changes. v28 requires
model rollout to be staged, measured, and reversible.

## Feature-Flagged AI Releases

Feature flags let AOIS-P separate deploy from release. The plan holds release
when feature flags are missing, unsafe, or not reversible.

## Build

Inspect:

```bash
sed -n '1,760p' release-safety/aois-p/delivery-release-controls.plan.json
sed -n '1,420p' examples/validate_delivery_release_controls_plan.py
sed -n '1,260p' examples/simulate_delivery_release_controls.py
```

Compile:

```bash
python3 -m py_compile examples/validate_delivery_release_controls_plan.py examples/simulate_delivery_release_controls.py
```

Validate:

```bash
python3 examples/validate_delivery_release_controls_plan.py
```

Simulate:

```bash
python3 examples/simulate_delivery_release_controls.py
```

Expected:

```json
{
  "passed_cases": 16,
  "score": 1.0,
  "status": "pass",
  "total_cases": 16
}
```

## Ops Lab

1. Open the delivery release controls plan.
2. Find `pipeline_stages`.
3. Confirm each stage blocks on failure.
4. Find `decision_gates`.
5. Confirm every gate has a release case.
6. Find `case_defaults`.
7. Confirm the default release is reviewed, least-privilege, tested, signed, approved, healthy, reversible, staged, and guarded.
8. Find `release_cases`.
9. Confirm each override isolates one release risk.
10. Run the validator.
11. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Change `case_defaults.workflow_permissions` to `write_all`.
2. Confirm the simulator no longer allows the first case.
3. Restore the value.
4. Remove `provenance_attestation_review` from live release checks.
5. Confirm validation fails.
6. Restore the check.
7. Change `missing_digest_blocked.overrides.artifact_digest` to a `sha256:` value.
8. Confirm the simulator no longer blocks missing digest.
9. Restore the value.
10. Change `feature_flag_unsafe_held.overrides.feature_flag_status` to `guarded`.
11. Confirm the simulator no longer holds the feature-flag case.
12. Restore the value.

## Testing

The validator checks:

- no live CI, build, signing, deploy, rollout, flag, model, network, provider, command, or tool runtime is enabled
- source notes are current for May 1, 2026
- release scope controls are explicit
- required release controls are true
- release dimensions are present
- pipeline stages are complete
- decision gates are complete
- defaults describe a safe candidate
- every decision has a release case
- live-release review checks are listed

The simulator checks:

- a fully gated release candidate is allowed
- unreviewed branch is blocked
- overprivileged workflow is blocked
- failed dependency review is blocked
- failed tests are blocked
- failed AOIS policy tests are blocked
- failed security scan is blocked
- missing digest is blocked
- missing provenance is blocked
- unsigned artifact is blocked
- unverified signature is blocked
- missing environment approval is blocked
- degraded health holds rollout
- missing rollback blocks release
- unstaged model rollout is held
- unsafe feature flag is held

## Common Mistakes

- treating CI as release safety by itself
- letting broad workflow permissions ship production changes
- testing code but not AOIS policy behavior
- signing without verifying
- approving an environment without release evidence
- rolling out without health gates
- treating rollback as optional
- changing model behavior without staged rollout
- deploying AI behavior without feature flags

## Troubleshooting

If validation fails:

- read the `missing` list
- restore false runtime flags
- restore source notes and dates
- restore required controls
- restore pipeline stages
- restore live-release review checks

If simulation fails:

- compare `decision` to `expected_decision`
- inspect the case override
- inspect `case_defaults`
- confirm the decision order matches the release risk
- confirm the expected operator action matches the gate

## Benchmark

Run:

```bash
python3 -m py_compile examples/validate_delivery_release_controls_plan.py examples/simulate_delivery_release_controls.py
python3 examples/validate_delivery_release_controls_plan.py
python3 examples/simulate_delivery_release_controls.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- CI, workflow, build, signing, deploy, rollout, traffic, flag, model, network, and provider flags

## Architecture Defense

Defend this design:

- release safety is modeled before real CI/CD automation
- delivery checks include AOIS product and policy regressions
- artifact identity and provenance are separate from signatures
- signatures must be verified, not merely produced
- environment approval is separate from test pass
- rollout health and rollback readiness are release gates
- model rollout and feature flags are first-class AI release controls
- AOIS-P remains separated from primary AOIS

## 4-Layer Tool Drill

Explain the v28 work at four layers:

- source: reviewed branch, least-privilege workflow, dependency review
- build: tests, policy regressions, scans, digest, provenance, signature
- release: approval, evidence, rollout strategy, health, rollback
- AI behavior: model rollout and feature flags

## 4-Level System Explanation Drill

Explain v28 at four levels:

- beginner: AOIS-P should not ship unless the release checks pass
- practitioner: the pipeline blocks or holds releases based on tests, evidence, approval, health, rollback, model, and flag controls
- engineer: the simulator evaluates one release risk at a time and returns promote, block, or hold
- architect: AOIS-P separates build integrity, release approval, rollout control, and AI behavior release so unsafe changes cannot bypass product and policy safeguards

## Failure Story

A team merges a small dashboard change and ships it directly after unit tests.
The workflow has broad write permissions, the artifact is not tied to a digest,
no provenance exists, the image signature is not verified, and the feature flag
turns on the new AI behavior for every tenant. The rollout health degrades, but
there is no rollback target.

v28 prevents this by requiring release evidence before promotion and by holding
or blocking unsafe rollout, model, and feature-flag states.

## Mastery Checkpoint

You are ready to move on when you can:

- trace a release case through each gate
- explain why tests alone are insufficient release safety
- explain digest, provenance, signing, and verification as separate controls
- explain why model rollout and feature flags belong in delivery
- pass validation and simulation without live CI/CD infrastructure

## Connection Forward

v29 builds on v28 by tracking experiments and model delivery evidence over
time. Once AOIS-P can block unsafe releases, it needs to compare behavior
changes and explain why a model or AI behavior rollout was accepted.

## Source Notes

Checked 2026-05-02.

- SLSA specification v1.2: used for provenance, verification, build-track, source-track, and supply-chain security language.
- Sigstore documentation: used for artifact signing, identity-bound certificates, transparency log, and signature verification concepts.
- OpenAI safety best-practices guidance: used for AI behavior release safety and adversarial testing context.
- v28 is a local release-control simulation. It does not run CI/CD, sign artifacts, contact registries, deploy workloads, or call providers.
