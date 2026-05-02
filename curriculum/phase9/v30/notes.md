# v30 - Internal Platform Patterns

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no platform
runtime, no developer portal, no service catalog, no platform API, no template
engine, no CLI invocation, no infrastructure provisioning, no Kubernetes apply,
no GitOps sync, no workflow run, no database, no network call, no provider call,
no persistent storage

## What This Builds

This version builds a local internal platform pattern contract:

- `platform/aois-p/internal-platform-patterns.plan.json`
- `examples/validate_internal_platform_patterns_plan.py`
- `examples/simulate_internal_platform_patterns.py`

It teaches:

- internal platform capability catalogs
- self-service abstractions
- developer portal entries
- platform API contracts
- golden path templates
- infrastructure abstraction
- policy, security, cost, tenant, and permission boundaries
- observability, release, and model-delivery integration
- lifecycle and deprecation controls
- support ownership and support SLOs

## Why This Exists

v28 and v29 made AOIS-P release and model-delivery behavior traceable. Without
platform patterns, every team would still rebuild the same controls differently.

The central platform question is:

```text
Given a requested platform capability, user persona, interface, owner,
documentation, API contract, golden path template, policy defaults, security,
cost, observability, release integration, model-delivery integration, tenant
boundary, approval, lifecycle, and support SLO, should AOIS-P publish, block,
or hold the self-service capability?
```

v30 answers that question locally. It does not run Backstage, start a platform
API, render templates, provision infrastructure, apply Kubernetes resources, or
sync GitOps state.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state -> scope access -> release changes safely -> track model and behavior delivery evidence -> package repeated controls as internal platform capabilities`

v30 consumes Phase 9:

- v28 release controls become reusable delivery capabilities
- v29 model-delivery tracking becomes reusable model platform capability
- Phase 8 access and visibility become platform defaults
- repeated AOIS controls become self-service patterns

The output is a platform decision: publish, block, or hold.

## Learning Goals

By the end of this version you should be able to:

- explain the difference between app engineering and platform engineering
- define a platform capability catalog
- design self-service interfaces without hiding ownership
- distinguish a developer portal from a platform API
- explain golden path templates
- keep infrastructure details behind stable contracts
- require policy, security, cost, tenancy, and observability defaults
- connect platform capabilities to release and model-delivery controls
- block incomplete platform abstractions before adoption
- validate and simulate internal platform decisions locally

## Prerequisites

You should have completed:

- Phase 8 product visibility and policy-aware access
- `v28` delivery pipeline and release controls
- `v29` experiment and model delivery tracking

Required checks:

```bash
python3 -m py_compile examples/validate_internal_platform_patterns_plan.py examples/simulate_internal_platform_patterns.py
python3 examples/validate_internal_platform_patterns_plan.py
python3 examples/simulate_internal_platform_patterns.py
```

## Core Concepts

## Internal Platform

An internal platform is a product for internal users. It offers consistent ways
to request, configure, observe, and operate shared capabilities.

The platform is not "the cluster." It is the product layer over common
capabilities: catalog, APIs, templates, docs, support, governance, and
automation.

## Capability Catalog

The v30 catalog includes reusable AOIS-P capabilities:

- service starter
- observability bundle
- delivery pipeline bundle
- model delivery bundle
- policy access bundle
- cost budget bundle
- incident response bundle
- environment request

Each capability has an owner, interfaces, and approval posture.

## Self-Service Abstraction

Self-service does not mean no control. It means the platform packages controls
so teams can safely request capabilities without bespoke meetings and manual
instructions.

## Developer Portal

A portal helps users discover capabilities, docs, ownership, and onboarding
paths. v30 models portal entries but does not run a portal.

## Platform API

A platform API gives a structured way to request and observe capabilities. The
API contract must exist before automation can be trusted.

## Golden Path Template

A golden path template packages known-good defaults. For AOIS-P, those defaults
include telemetry, access policy, delivery gates, rollback, budget, and
incident-response wiring.

## Infrastructure Abstraction

The platform hides unnecessary provider details while preserving important
choices and observability. Product teams should consume a capability contract,
not own every implementation detail.

## Boundaries

Every capability needs policy, security, cost, tenant, and permission
boundaries. v30 blocks capabilities that make those boundaries optional.

## Release And Model Delivery Integration

Platform capabilities must inherit v28 release controls and v29 model-delivery
tracking when relevant. A reusable model platform capability is unsafe without
experiment tracking, registry linkage, feature flags, rollback, and risk
review.

## Build

Inspect:

```bash
sed -n '1,820p' platform/aois-p/internal-platform-patterns.plan.json
sed -n '1,460p' examples/validate_internal_platform_patterns_plan.py
sed -n '1,260p' examples/simulate_internal_platform_patterns.py
```

Compile:

```bash
python3 -m py_compile examples/validate_internal_platform_patterns_plan.py examples/simulate_internal_platform_patterns.py
```

Validate:

```bash
python3 examples/validate_internal_platform_patterns_plan.py
```

Simulate:

```bash
python3 examples/simulate_internal_platform_patterns.py
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

1. Open the internal platform patterns plan.
2. Find `capability_catalog`.
3. Confirm every capability has owner, interfaces, and approval posture.
4. Find `interface_catalog`.
5. Confirm portal, API, template, and CLI interfaces have contracts.
6. Find `case_defaults`.
7. Confirm the default capability is documented, versioned, guarded, observable, release-integrated, tenant-bound, and supported.
8. Find `platform_cases`.
9. Confirm each decision gate has a case.
10. Run the validator.
11. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Remove `model_delivery_bundle` from the capability catalog.
2. Confirm validation fails.
3. Restore the capability.
4. Change `case_defaults.owner` to an empty string.
5. Confirm the simulator no longer allows the first case.
6. Restore the owner.
7. Change `release_integration_missing_blocked.overrides.release_integration_status` to `complete`.
8. Confirm that case no longer blocks.
9. Restore the value.
10. Change `support_slo_missing_held.overrides.support_slo_status` to `defined`.
11. Confirm that case no longer holds.
12. Restore the value.

## Testing

The validator checks:

- no live platform, portal, catalog, API, template, CLI, infrastructure, Kubernetes, GitOps, workflow, database, network, provider, command, or tool runtime is enabled
- source notes are current for May 1, 2026
- platform scope controls are explicit
- required controls are true
- platform dimensions are present
- capability catalog is complete
- interface catalog is complete
- decision gates are complete
- defaults describe a complete self-service capability
- every platform decision has a case
- live platform review checks are listed

The simulator checks:

- complete self-service capability is allowed
- unknown capability is blocked
- deprecated capability is blocked
- missing owner is blocked
- missing docs are blocked
- missing API contract is blocked
- missing template is blocked
- policy failure is blocked
- security failure is blocked
- cost review is held
- missing observability is blocked
- missing release integration is blocked
- missing model-delivery integration is held
- missing tenant boundary is blocked
- missing required approval is blocked
- missing support SLO is held

## Common Mistakes

- treating platform engineering as a ticket queue
- publishing templates with no owner
- building a portal without API contracts
- creating self-service that bypasses policy
- hiding cost and quota controls
- omitting observability from golden paths
- making release controls optional
- making model delivery controls separate from platform capabilities
- leaving support ownership undefined

## Troubleshooting

If validation fails:

- read the `missing` list
- restore false runtime flags
- restore source notes and dates
- restore required controls
- restore capability and interface catalogs
- restore live platform review checks

If simulation fails:

- compare `decision` to `expected_decision`
- inspect the case override
- inspect `case_defaults`
- confirm the capability exists in the catalog
- confirm lifecycle, owner, docs, API, template, policy, security, cost, observability, release, model, tenant, approval, and support state

## Benchmark

Run:

```bash
python3 -m py_compile examples/validate_internal_platform_patterns_plan.py examples/simulate_internal_platform_patterns.py
python3 examples/validate_internal_platform_patterns_plan.py
python3 examples/simulate_internal_platform_patterns.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- platform, portal, catalog, API, template, CLI, infra, Kubernetes, GitOps, network, and provider flags

## Architecture Defense

Defend this design:

- platform capabilities are treated as products
- catalog ownership is required
- docs, APIs, and templates are separate controls
- self-service still enforces policy and security
- cost, tenant, and permission boundaries are explicit
- observability is part of every platform capability
- v28 release controls and v29 model delivery controls are reusable defaults
- unsupported or deprecated capabilities are blocked
- support SLOs are required before broad adoption
- AOIS-P remains separated from primary AOIS

## 4-Layer Tool Drill

Explain v30 at four layers:

- catalog: capability, owner, interface, lifecycle
- contract: docs, API, template, request shape
- guardrails: policy, security, cost, tenant, approval
- operations: observability, release integration, model delivery, support SLO

## 4-Level System Explanation Drill

Explain v30 at four levels:

- beginner: teams get safe reusable AOIS capabilities instead of rebuilding them
- practitioner: self-service capabilities need catalog ownership, docs, APIs, templates, guardrails, and support
- engineer: the simulator evaluates one missing platform control at a time and returns publish, block, or hold
- architect: AOIS-P packages governance, delivery, model tracking, observability, access, and cost controls into reusable platform abstractions with stable contracts

## Failure Story

Three teams copy an old AOIS starter template. One version lacks tenant
boundaries, another skips release-gate wiring, and the third has no owner or
support SLO. A model behavior rollout bypasses v29 tracking because the template
never connected the model-delivery bundle.

v30 prevents this by requiring catalog ownership, docs, API contracts, golden
path templates, guardrails, release integration, model-delivery integration,
tenant boundaries, approval records, lifecycle state, and support SLOs before
publishing self-service capabilities.

## Mastery Checkpoint

You are ready to move on when you can:

- distinguish app engineering from platform engineering
- define a platform capability and its owner
- explain why docs, API, and template are separate platform controls
- explain how release and model-delivery controls become reusable capabilities
- trace a platform request through allow, block, and hold decisions
- pass validation and simulation without live platform infrastructure

## Connection Forward

Phase 9 is complete. AOIS-P can now model delivery safety, model delivery
evidence, and reusable internal platform abstractions.

v31 begins Phase 10 by extending AOIS into multimodal inputs while preserving
the rigor built through observability, governance, product access, delivery,
and platform controls.

## Source Notes

Checked 2026-05-02.

- SLSA specification v1.2 and Sigstore documentation: used for reusable release, provenance, signing, and verification controls.
- OpenTelemetry trace concepts documentation: used for platform observability and trace vocabulary.
- OWASP Application Security Verification Standard project page: used for secure product-control and verification framing.
- v30 is a local internal-platform contract. It does not provision infrastructure, run templates, publish APIs, sync GitOps, or call providers.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v30 Introduction](introduction.md)
- Next: [v30 Lab](lab.md)
<!-- AOIS-NAV-END -->
