# v30 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether an internal platform
capability should be published, blocked, or held.

## Primary Checks

1. Confirm the decision is for `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm capability is in the catalog.
4. Confirm lifecycle status is active.
5. Confirm owner is assigned.
6. Confirm documentation is complete.
7. Confirm platform API or resource contract exists.
8. Confirm golden path template exists.
9. Confirm policy defaults pass.
10. Confirm security boundaries pass.
11. Confirm cost or quota review is approved.
12. Confirm observability contract exists.
13. Confirm v28 release controls are connected.
14. Confirm model-related capabilities are connected to v29 model-delivery tracking.
15. Confirm tenant and permission boundaries exist.
16. Confirm required approval is recorded.
17. Confirm support SLO is defined.
18. Confirm no live platform, portal, catalog, API, template, CLI, infrastructure, Kubernetes, GitOps, network, or provider runtime flags are enabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_internal_platform_patterns_plan.py
python3 examples/simulate_internal_platform_patterns.py
```

Decision handling:

- `allow_self_service_capability`: publish self-service capability.
- `block_unknown_capability`: register capability or reject request.
- `block_deprecated_capability`: route to supported capability.
- `block_missing_owner`: assign platform owner.
- `block_missing_docs`: write onboarding docs.
- `block_missing_api_contract`: define platform API contract.
- `block_missing_template`: create golden path template.
- `block_policy_boundary`: repair policy defaults.
- `block_security_boundary`: repair security boundary.
- `hold_cost_review`: complete cost and quota review.
- `block_observability_missing`: add observability contract.
- `block_release_integration_missing`: connect v28 release controls.
- `hold_model_delivery_integration`: connect v29 model-delivery tracking.
- `block_tenant_boundary_missing`: define tenant and permission boundaries.
- `block_approval_missing`: request platform capability approval.
- `hold_support_slo_missing`: define support SLO.

Escalate to a platform owner if:

- a capability has no owner
- self-service bypasses policy or security boundaries
- cost or tenant controls are missing
- release or model-delivery integrations are absent
- support ownership is unclear
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v30 Lab](lab.md)
- Next: [v30 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
