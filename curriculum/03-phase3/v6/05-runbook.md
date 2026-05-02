# v6 Runbook

Authoring status: authored

## Purpose

Use this runbook when the Kubernetes plan validator fails or someone wants to apply manifests.

## Primary Checks

Validate without applying:

```bash
python3 examples/validate_k8s_plan.py
```

Inspect:

```bash
sed -n '1,220p' k8s/aois-p/deployment.yaml
sed -n '1,160p' k8s/aois-p/resource-quota.yaml
```

## Recovery Steps

If validation fails:

- read the `missing` list
- restore the referenced manifest field
- rerun the validator

If applying is requested:

- stop
- confirm target cluster
- confirm namespace is `aois-p`
- confirm resource budget
- confirm image availability
- get explicit approval
- record resource usage after apply

If resources appear unexpectedly:

- identify whether they are portfolio-owned
- do not delete primary AOIS resources
- ask before changing live cluster state
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v6 Lab](04-lab.md)
- Next: [v6 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
