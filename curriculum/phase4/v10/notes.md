# v10 - Managed Model Layer Without Cloud Calls

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: plan and validation only, no AWS credentials, no Bedrock call, no network

## What This Builds

This version builds a managed model layer plan:

- `cloud/aws/bedrock-model-layer.plan.json`
- `examples/validate_managed_model_plan.py`

It teaches:

- managed model provider boundary
- request and response contract
- budget gating
- credential gating
- security inspection before provider use
- trace and eval requirements
- why cloud calls require explicit approval

## Why This Exists

Enterprise model services can reduce infrastructure burden, but they introduce new boundaries:

- credentials
- network egress
- provider terms
- latency
- cost
- data exposure
- model/version drift

AOIS needs to reason about the managed model layer before invoking it.

## AOIS Connection

The AOIS path is now:

`security inspection -> route decision -> managed model plan -> provider gate -> future cloud call`

Phase 1 created structured AI contracts.
Phase 4 maps that contract to an enterprise managed model layer without using credentials or spend.

## Learning Goals

By the end of this version you should be able to:

- explain a managed model layer
- explain why provider credentials are gated
- explain why budget approval is required
- explain what request contract must be preserved
- explain what controls must be checked before cloud inference
- validate the plan locally without cloud access

## Resource Gate

Do not run:

```bash
aws bedrock-runtime invoke-model
aws bedrock list-foundation-models
```

Do not add:

- AWS credentials
- real model IDs
- real provider API keys
- paid inference
- network calls

Allowed:

- inspect plan JSON
- run local validator

Live Bedrock or any managed model call requires explicit approval, request limit, budget, credentials plan, and source-currency check against official provider documentation.

## Prerequisites

You should have completed:

- Phase 1 structured intelligence core
- Phase 2 security foundations
- Phase 3 infrastructure/GitOps planning

Required checks:

```bash
python3 -m py_compile examples/validate_managed_model_plan.py
python3 examples/validate_managed_model_plan.py
```

## Core Concepts

## Managed Model Layer

A managed model layer is an external service that hosts model inference for you.

You do not manage GPUs or serving runtime directly, but you must manage:

- credentials
- request shape
- output validation
- cost
- latency
- data exposure

## Provider Gate

The provider gate prevents cloud inference until approval exists.

In this plan:

```json
"provider_call_made": false
```

## Budget Gate

The budget gate prevents unbounded spend.

In this plan:

```json
"approved": false,
"max_spend_usd": 0
```

## Request Contract

The request contract preserves the AOIS structured input/output shape.

It prevents provider integration from becoming unstructured prompt sprawl.

## Source Currency

Managed provider APIs change.

Before live use, check official provider documentation for current model IDs, request formats, pricing, quotas, and data-use terms.

## Build

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

Expected:

```json
{
  "cloud_call_made": false,
  "credentials_used": false,
  "status": "pass"
}
```

## Ops Lab

Answer:

1. Which file defines the managed model plan?
2. Which field proves no provider call happened?
3. Which field proves credentials are not needed for this lesson?
4. Which budget value prevents spend?
5. Which controls must remain true before future provider use?

Answer key:

1. `cloud/aws/bedrock-model-layer.plan.json`
2. `provider_call_made=false`
3. `credentials_required_for_this_lesson=false`
4. `max_spend_usd=0`
5. security inspection, provider gate, trace ID, eval baseline, and resource usage record

## Break Lab

Do not skip this.

### Option A - Budget Approved Too Early

In a scratch copy, set:

```json
"approved": true
```

Expected risk:

- cloud inference could be treated as allowed before budget and credential controls exist

### Option B - Remove Security Inspection

In a scratch copy, set:

```json
"security_inspection_required": false
```

Expected risk:

- prompt-injection or secret-like content could cross the provider boundary

## Testing

The version passes when:

1. validator compiles
2. validator returns `status=pass`
3. cloud call remains false
4. credentials used remains false
5. budget approval remains false
6. no network or provider command runs

## Common Mistakes

- adding cloud credentials to repo files
- using real model IDs before source-currency review
- treating managed inference as free
- skipping security inspection
- skipping eval baseline before provider integration
- assuming provider output will match AOIS contract automatically

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_managed_model_plan.py
```

Read `missing`, inspect the plan JSON, and restore the gated field.

If live provider use is requested:

- stop
- check official provider docs
- define model and request format
- define max requests and spend
- define credential storage
- define logging/redaction rules
- get explicit approval

## Benchmark

Measure:

- validator compile result
- validator status
- whether cloud call happened
- whether credentials were used
- whether spend was approved
- repo disk footprint
- memory snapshot

## Architecture Defense

Why managed model planning before provider calls?

Because enterprise model services move risk to credentials, cost, latency, data exposure, quotas, and provider contracts.

Why no real model ID?

Because model names and availability can change; live use must check official docs first.

Why preserve eval baseline?

Because managed models should be compared against local expected behavior.

## 4-Layer Tool Drill

Tool: managed model layer

1. Plain English
It lets AOIS use a cloud-hosted model.

2. System Role
It becomes a possible external inference route after security, budget, and provider gates pass.

3. Minimal Technical Definition
It is a provider API boundary that accepts structured requests and returns model output under provider-specific rules.

4. Hands-on Proof
The validator confirms the plan has request/output contracts and no cloud call, credentials, or spend.

## 4-Level System Explanation Drill

1. Simple English
AOIS can plan cloud model use without using cloud.

2. Practical Explanation
I can inspect the plan and prove no credentials, network, or spend are involved.

3. Technical Explanation
`v10` adds a managed model layer plan JSON and a local validator.

4. Engineer-Level Explanation
AOIS now separates enterprise model-provider integration design from provider execution, preserving security inspection, provider gating, budget controls, traceability, and eval requirements before cloud inference.

## Failure Story

Representative failure:

- Symptom: a cloud model call costs money and sends sensitive input before review
- Root cause: provider call was wired before security and budget gates
- Fix: restore provider gate and require explicit approval
- Prevention: validate managed model plan before live integration
- What this taught me: managed inference is still an operational boundary

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v10` solve in AOIS?
2. What is a managed model layer?
3. Why are credentials gated?
4. Why is budget gated?
5. Why is security inspection required?
6. Why is source-currency review required before live provider use?
7. What does `provider_call_made=false` prove?
8. Why is eval baseline required before provider integration?
9. What should happen before a real Bedrock-style call?
10. Explain managed model layer using the 4-layer tool rule.
11. Explain `v10` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v10` solve in AOIS?

It plans enterprise managed model integration without using credentials, network, or spend.

2. What is a managed model layer?

A provider-hosted inference service that AOIS can call instead of hosting models itself.

3. Why are credentials gated?

Credentials can grant access to paid services and sensitive cloud actions.

4. Why is budget gated?

Provider inference can cost money per request or token.

5. Why is security inspection required?

To prevent risky input or secret-like content from crossing provider boundaries.

6. Why is source-currency review required before live provider use?

Provider APIs, model IDs, pricing, quotas, and data-use terms change.

7. What does `provider_call_made=false` prove?

No external model provider was contacted.

8. Why is eval baseline required before provider integration?

So provider output can be compared against known expected behavior.

9. What should happen before a real Bedrock-style call?

Check official docs, define model/request format, set budget/request limit, secure credentials, and get explicit approval.

10. Explain managed model layer using the 4-layer tool rule.

- Plain English: it gives AOIS access to a cloud-hosted model.
- System Role: it is an external inference route.
- Minimal Technical Definition: it is a provider API boundary for model inference.
- Hands-on Proof: the validator confirms plan controls without cloud calls.

11. Explain `v10` using the 4-level system explanation rule.

- Simple English: AOIS can plan cloud model use safely.
- Practical explanation: I can validate no credentials, spend, or network are used.
- Technical explanation: `v10` adds a Bedrock-style plan JSON and validator.
- Engineer-level explanation: AOIS now has enterprise model-layer design separated from provider execution, preserving budget, security, traceability, and eval gates.

## Connection Forward

`v10` plans managed model inference.

`v10.5` examines managed cloud agent services and their tradeoffs versus building the agent runtime inside AOIS.
