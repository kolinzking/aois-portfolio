# v9 Runbook

Authoring status: authored

## Purpose

Use this runbook when autoscaling validation fails or someone wants to enable live scaling.

## Primary Checks

Validate:

```bash
python3 examples/validate_autoscaling_plan.py
```

Inspect:

```bash
sed -n '1,200p' k8s/aois-p/hpa.yaml
sed -n '1,220p' k8s/aois-p/keda-scaledobject.plan.yaml
```

## Recovery Steps

If validation fails:

- read `missing`
- restore max replicas cap
- rerun the validator

If live scaling is requested:

- stop
- estimate CPU/RAM per replica
- confirm max replica count
- confirm dependency capacity
- get explicit approval
- record resource usage after apply
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v9 Lab](lab.md)
- Next: [v9 Failure Story](failure-story.md)
<!-- AOIS-NAV-END -->
