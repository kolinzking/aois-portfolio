# v29 - Experiment And Model Delivery Tracking

Estimated time: 6-8 focused hours

Authoring status: authored

Resource posture: local plan and deterministic simulation only, no experiment
tracker, no model registry, no training job, no evaluation job, no model
download, no model upload, no model promotion, no traffic shift, no
feature-flag service call, no rollout controller, no database, no network call,
no provider call, no persistent storage

## What This Builds

This version builds a local experiment and model-delivery tracking contract:

- `release-safety/aois-p/experiment-model-delivery.plan.json`
- `examples/validate_experiment_model_delivery_plan.py`
- `examples/simulate_experiment_model_delivery.py`

It teaches:

- experiment design records
- champion and challenger version comparison
- dataset version pinning
- metric catalogs
- guardrail metrics
- offline evaluation evidence
- rollout evidence
- model registry links
- feature-flag links
- model rollback targets
- approval and risk-review records

## Why This Exists

v28 can decide whether a release candidate should promote, block, or hold. AI
delivery needs one more layer: evidence about what behavior changed, how it was
measured, and why the candidate is better or safer than the current baseline.

The central model-delivery question is:

```text
Given an experiment hypothesis, baseline version, candidate version, dataset
version, metric deltas, guardrail status, rollout evidence, registry record,
release gate, feature flag, rollback target, approval, and risk review, should
AOIS-P promote, block, or hold the model or behavior change?
```

v29 answers that question locally. It does not start a tracking server, model
registry, training job, evaluation job, rollout controller, or feature-flag
service.

## AOIS Connection

The AOIS path is now:

`observe -> trace -> stream -> measure -> respond -> test failure -> govern -> plan tool use -> account for cost -> route by budget -> govern tool exposure -> preserve workflow state -> orchestrate next action -> evaluate connected behavior -> control autonomy mode -> coordinate agent roles -> bound execution -> show operators the state -> scope access -> release changes safely -> track model and behavior delivery evidence`

v29 consumes v28 release controls:

- release gate status
- feature-flag readiness
- rollback readiness
- model rollout discipline
- release evidence

The output is a model-delivery decision: promote, block, or hold.

## Learning Goals

By the end of this version you should be able to:

- define an experiment before comparing model versions
- explain why every candidate needs a baseline
- pin dataset versions for evaluation evidence
- distinguish offline evaluation from rollout evidence
- build a metric catalog with quality, latency, cost, safety, policy, and tenancy guardrails
- explain champion/challenger delivery
- require model registry records before promotion
- link model delivery to release gates and feature flags
- block regressions and hold incomplete evidence
- validate and simulate model delivery decisions locally

## Prerequisites

You should have completed:

- Phase 5 model adaptation and inference lessons
- Phase 8 product visibility and access lessons
- `v28` delivery pipeline and release controls

Required checks:

```bash
python3 -m py_compile examples/validate_experiment_model_delivery_plan.py examples/simulate_experiment_model_delivery.py
python3 examples/validate_experiment_model_delivery_plan.py
python3 examples/simulate_experiment_model_delivery.py
```

## Core Concepts

## Experiment Design

An experiment needs a hypothesis, not just a model name. The hypothesis states
what behavior should improve and what evidence would justify delivery.

## Baseline And Candidate

The current champion model or behavior is the baseline. The challenger is the
candidate. v29 blocks delivery when either version is missing because there is
nothing defensible to compare.

## Dataset Version

Evaluation evidence needs a pinned dataset version. Without it, the team cannot
reproduce why a candidate passed or failed.

## Metric Catalog

The metric catalog defines what matters:

- quality score
- p95 latency
- cost per 1,000 tokens
- safety violation rate
- policy regression count
- tenant isolation failures

The candidate must improve quality enough while staying inside latency, cost,
safety, policy, and tenancy boundaries.

## Guardrails

Guardrails are non-negotiable controls. A candidate that improves quality but
regresses tenant isolation or policy behavior is blocked.

## Offline Evaluation

Offline evaluation checks the candidate before rollout. It is necessary but not
sufficient because live behavior still needs rollout evidence.

## Rollout Evidence

Rollout evidence shows how the candidate behaved during staged exposure. v29
holds delivery when sample size or rollout evidence is incomplete.

## Model Registry Record

The registry record connects versions, aliases, tags, annotations, and delivery
metadata. v29 blocks promotion when the registry record is incomplete.

## Feature Flag Link

Feature flags connect delivery to controlled exposure. v29 holds delivery when
the flag is unsafe or not reversible.

## Approval And Risk Review

Model delivery needs human approval and risk review. A candidate with good
metrics still waits if risk review is pending.

## Build

Inspect:

```bash
sed -n '1,760p' release-safety/aois-p/experiment-model-delivery.plan.json
sed -n '1,460p' examples/validate_experiment_model_delivery_plan.py
sed -n '1,260p' examples/simulate_experiment_model_delivery.py
```

Compile:

```bash
python3 -m py_compile examples/validate_experiment_model_delivery_plan.py examples/simulate_experiment_model_delivery.py
```

Validate:

```bash
python3 examples/validate_experiment_model_delivery_plan.py
```

Simulate:

```bash
python3 examples/simulate_experiment_model_delivery.py
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

## Ops Lab

1. Open the experiment model delivery plan.
2. Find `metric_catalog`.
3. Confirm each metric blocks on regression.
4. Find `evidence_stages`.
5. Confirm each stage blocks on missing evidence.
6. Find `case_defaults`.
7. Confirm the default candidate is documented, versioned, evaluated, guarded, approved, and reversible.
8. Find `delivery_cases`.
9. Confirm each decision gate has a case.
10. Run the validator.
11. Run the simulator.

## Break Lab

Break the plan locally, then restore it:

1. Change `case_defaults.hypothesis_status` to `missing`.
2. Confirm the simulator no longer allows the first case.
3. Restore the value.
4. Remove `quality_score` from the metric catalog.
5. Confirm validation fails.
6. Restore the metric.
7. Change `metric_regression_blocked.overrides.metric_delta.quality_score` to `0.05`.
8. Confirm the simulator no longer blocks that case.
9. Restore the value.
10. Change `risk_review_pending_held.overrides.risk_status` to `accepted`.
11. Confirm the simulator no longer holds that case.
12. Restore the value.

## Testing

The validator checks:

- no live tracker, registry, training, eval, rollout, flag, network, provider, command, or tool runtime is enabled
- source notes are current for May 1, 2026
- tracking scope controls are explicit
- required controls are true
- delivery dimensions are present
- metric catalog is complete
- evidence stages are complete
- decision gates are complete
- defaults describe a safe candidate
- every decision has a delivery case
- live model-delivery review checks are listed

The simulator checks:

- fully evidenced candidate is allowed
- missing hypothesis is blocked
- missing baseline is blocked
- missing candidate is blocked
- missing dataset version is blocked
- failed offline evaluation is blocked
- metric regression is blocked
- guardrail regression is blocked
- insufficient sample size is held
- missing rollout evidence is held
- incomplete registry record is blocked
- failed release gate is blocked
- unsafe feature flag is held
- missing rollback is blocked
- missing approval is blocked
- pending risk review is held

## Common Mistakes

- promoting a model because it is newer
- comparing candidates without a pinned dataset version
- tracking quality but not latency or cost
- treating safety, policy, and tenant isolation as soft metrics
- relying on offline eval without rollout evidence
- recording experiments without model registry links
- rolling out behavior without feature flags
- approving delivery before risk review

## Troubleshooting

If validation fails:

- read the `missing` list
- restore false runtime flags
- restore source notes and dates
- restore required controls
- restore metric catalog and evidence stages
- restore live model-delivery checks

If simulation fails:

- compare `decision` to `expected_decision`
- inspect the case override
- inspect `case_defaults`
- inspect metric deltas
- confirm guardrail metrics are zero
- confirm sample size, rollout evidence, registry, release gate, flag, rollback, approval, and risk status

## Benchmark

Run:

```bash
python3 -m py_compile examples/validate_experiment_model_delivery_plan.py examples/simulate_experiment_model_delivery.py
python3 examples/validate_experiment_model_delivery_plan.py
python3 examples/simulate_experiment_model_delivery.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- tracker, registry, training, eval, model, rollout, feature flag, network, and provider flags

## Architecture Defense

Defend this design:

- experiments are defined before delivery
- champion/challenger versions are explicit
- dataset versions are pinned
- quality, latency, cost, safety, policy, and tenancy are measured together
- offline evaluation and rollout evidence are separate
- model registry records are required
- v28 release gates still apply
- feature flags and rollback are delivery controls
- approval and risk review are required
- AOIS-P remains separated from primary AOIS

## 4-Layer Tool Drill

Explain the v29 work at four layers:

- experiment: hypothesis, dataset, baseline, candidate
- evaluation: metric deltas and guardrail results
- delivery: registry, release gate, feature flag, rollback
- governance: approval, risk review, audit-ready decision

## 4-Level System Explanation Drill

Explain v29 at four levels:

- beginner: do not ship a model change unless evidence says it is better and safe
- practitioner: compare champion and challenger with pinned data, metrics, guardrails, rollout evidence, and approvals
- engineer: the simulator evaluates one missing or failed evidence item at a time and returns promote, block, or hold
- architect: AOIS-P separates experiment tracking, model registry, release gates, rollout evidence, and risk review so AI behavior changes are traceable and defensible

## Failure Story

A team ships a new model alias because offline quality looks better. They do
not record the dataset version, the baseline model, rollout sample size, or
feature-flag state. Latency and cost rise, tenant-isolation regressions appear,
and the team cannot prove which experiment justified the promotion.

v29 prevents this by requiring experiment design, version comparison, metric
catalog, guardrails, rollout evidence, registry links, release gates, flags,
rollback, approval, and risk review before delivery.

## Mastery Checkpoint

You are ready to move on when you can:

- define a model-delivery experiment
- explain champion/challenger comparison
- explain why dataset versions matter
- distinguish metric regression from guardrail regression
- explain why rollout evidence can hold a candidate
- pass validation and simulation without live model infrastructure

## Connection Forward

v30 completes Phase 9 by turning repeated AOIS delivery patterns into an
internal platform: self-service abstractions, platform APIs, and infrastructure
abstraction for reusable AOIS capabilities.

## Source Notes

Checked 2026-05-02.

- OpenAI evals documentation: used for current evaluation vocabulary around datasets, samples, graders, and measured model behavior.
- OpenAI safety best-practices guidance: used for guardrail, adversarial testing, and safety-review framing.
- SLSA specification v1.2: used for release evidence, provenance, and verification language that connects model delivery to release controls.
- v29 is a local experiment and model-delivery simulation. It does not call eval services, train models, upload datasets, use a model registry, or call providers.
