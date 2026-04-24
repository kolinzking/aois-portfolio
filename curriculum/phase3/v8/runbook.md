# v8 Runbook

Authoring status: authored

## Purpose

Use this runbook when GitOps validation fails or live ArgoCD sync is being considered.

## Primary Checks

Validate:

```bash
python3 examples/validate_gitops_plan.py
```

Inspect:

```bash
sed -n '1,220p' gitops/argocd/aois-p-application.yaml
```

## Recovery Steps

If validation fails:

- read `missing`
- restore the referenced field
- rerun the validator

If live sync is requested:

- stop
- replace placeholder repo URL
- confirm target cluster
- confirm namespace `aois-p`
- confirm manual sync policy
- get explicit approval
- record resource usage after sync
