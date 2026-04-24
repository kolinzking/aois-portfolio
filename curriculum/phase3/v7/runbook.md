# v7 Runbook

Authoring status: authored

## Purpose

Use this runbook when Helm chart validation fails or a chart install is being considered.

## Primary Checks

Validate:

```bash
python3 examples/validate_helm_plan.py
```

Inspect:

```bash
sed -n '1,120p' charts/aois-p/Chart.yaml
sed -n '1,220p' charts/aois-p/values.yaml
```

## Recovery Steps

If validation fails:

- read `missing`
- restore the referenced file or value
- rerun the validator

If install is requested:

- stop
- render/review chart first
- confirm namespace `aois-p`
- confirm resource budget
- get explicit approval
- record resource usage after install
