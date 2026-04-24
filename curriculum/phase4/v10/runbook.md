# v10 Runbook

Authoring status: authored

## Purpose

Use this runbook when the managed model plan fails validation or live provider use is being considered.

## Primary Checks

Validate:

```bash
python3 examples/validate_managed_model_plan.py
```

Inspect:

```bash
sed -n '1,220p' cloud/aws/bedrock-model-layer.plan.json
```

## Recovery Steps

If validation fails:

- read `missing`
- restore gated fields
- rerun the validator

If live provider use is requested:

- stop
- check official provider docs
- define model and request format
- define max requests and max spend
- define credential storage
- define logging/redaction rules
- get explicit approval
