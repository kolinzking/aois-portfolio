# v30 Benchmark

Authoring status: authored

## Measurements

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
- platform, portal, catalog, API, template, CLI, infrastructure, Kubernetes, GitOps, network, and provider flags

## Interpretation

Pass means:

- platform scope is local and AOIS-P only
- capability catalog is complete
- interface catalog is complete
- self-service capability defaults are complete
- every platform decision has a case
- ownership, docs, API contracts, templates, policy, security, cost, observability, release, model delivery, tenant, approval, lifecycle, and support gates work
- no live platform runtime is enabled

Fail means the platform abstraction contract is incomplete. Fix the plan or
simulator before beginning Phase 10.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v30 Failure Story](failure-story.md)
- Next: [v30 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
