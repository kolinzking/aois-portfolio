# v30 Failure Story

Authoring status: authored

## Symptom

Three teams build AOIS services from copied templates. One skips tenant
boundaries, one omits delivery gates, and one uses a model rollout path with no
experiment tracking. During an incident, no one knows who owns the template or
which team supports it.

## Root Cause

The organization had scripts and examples but no internal platform contract.
Capabilities were not cataloged, owners were unclear, docs drifted, API
contracts were missing, templates did not enforce policy defaults, and support
SLOs were never defined.

## Fix

v30 fixes the failure with internal platform patterns:

- capability catalog
- accountable owners
- docs and onboarding
- platform API contracts
- golden path templates
- policy, security, cost, tenant, and permission boundaries
- observability defaults
- v28 release integration
- v29 model-delivery integration
- approval records
- lifecycle and support SLO controls

## Prevention

Before live platform rollout:

- review the platform as a product
- review capability catalog entries
- review developer portal entries
- review platform API contracts
- review golden path templates
- review policy and security defaults
- review cost, quota, and tenant boundaries
- review observability wiring
- review release and model-delivery integrations
- review support SLOs and deprecation policy
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v30 Runbook](05-runbook.md)
- Next: [v30 Benchmark](07-benchmark.md)
<!-- AOIS-NAV-END -->
