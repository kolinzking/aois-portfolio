# v10 Lab

Authoring status: authored

## Build Lab

Inspect:

```bash
sed -n '1,220p' cloud/aws/bedrock-model-layer.plan.json
sed -n '1,220p' examples/validate_managed_model_plan.py
```

Compile:

```bash
python3 -m py_compile examples/validate_managed_model_plan.py
```

Run:

```bash
python3 examples/validate_managed_model_plan.py
```

Success state:

- status is `pass`
- cloud call is false
- credentials used is false
- budget approval is false

## Ops Lab

Answer:

1. what file defines the managed model plan?
2. what proves no cloud call happened?
3. what proves credentials were not used?
4. what prevents spend?
5. what controls must remain enabled?

## Break Lab

Use scratch copies only.

Set budget approval to true and explain why that is unsafe without request limits.

Disable security inspection and explain why that weakens the provider boundary.

## Explanation Lab

Answer:

1. what is a managed model layer?
2. why are credentials gated?
3. why is budget gated?
4. why is source-currency required?
5. why does eval baseline matter?

## Defense Lab

Defend:

`Managed inference should be planned before it is called.`

Your defense must mention:

- credentials
- spend
- data exposure
- latency
- provider docs
- eval baseline

## Benchmark Lab

Record:

- validator result
- cloud call status
- credentials status
- budget status
- repo footprint
