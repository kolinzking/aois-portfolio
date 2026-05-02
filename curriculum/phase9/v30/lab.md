# v30 Lab

Authoring status: authored

## Build Lab

Validate and simulate AOIS-P internal platform patterns without starting a
platform runtime, developer portal, service catalog, platform API, template
engine, CLI, infrastructure provisioner, Kubernetes apply, GitOps sync,
provider call, or network call.

Files:

- `platform/aois-p/internal-platform-patterns.plan.json`
- `examples/validate_internal_platform_patterns_plan.py`
- `examples/simulate_internal_platform_patterns.py`

Inspect:

```bash
sed -n '1,820p' platform/aois-p/internal-platform-patterns.plan.json
```

## Ops Lab

Run:

```bash
python3 -m py_compile examples/validate_internal_platform_patterns_plan.py examples/simulate_internal_platform_patterns.py
python3 examples/validate_internal_platform_patterns_plan.py
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

## Break Lab

Change one value at a time, run the validator or simulator, then restore the
plan:

- remove `environment_request` from `capability_catalog`
- remove `api` from `interface_catalog`
- change `case_defaults.documentation_status` to `missing`
- change `policy_boundary_blocked.overrides.policy_status` to `pass`
- change `model_delivery_integration_pending_held.overrides.model_delivery_status` to `complete`
- change `support_slo_missing_held.overrides.support_slo_status` to `defined`

## Explanation Lab

Explain why each case chooses its decision:

- complete self-service service starter publishes
- unknown capability blocks
- deprecated capability blocks
- missing owner blocks
- missing docs block
- missing API contract blocks
- missing template blocks
- policy boundary failure blocks
- security boundary failure blocks
- pending cost review holds
- missing observability blocks
- missing release integration blocks
- missing model delivery integration holds
- missing tenant boundary blocks
- missing approval blocks
- missing support SLO holds

## Defense Lab

Defend why v30 models internal platform patterns locally before running a
portal, catalog, platform API, or template engine. The system should prove
capability contracts and safety gates before self-service can provision or
mutate real infrastructure.
