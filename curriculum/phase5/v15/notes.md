# v15 - Fine-Tuning And Adaptation Without Training

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: adaptation plan and eval simulation only, no training job, no dataset upload, no model download, no GPU runtime

## What This Builds

This version builds a fine-tuning and adaptation plan:

- `inference/aois-p/fine-tuning-adaptation.plan.json`
- `examples/validate_fine_tuning_plan.py`
- `examples/simulate_adaptation_eval.py`

It teaches:

- no-tuning baseline
- prompt/routing adjustment before training
- LoRA-style adaptation awareness
- full fine-tune tradeoffs
- dataset cards
- train/validation/holdout splits
- eval before and after adaptation
- regression detection
- why adaptation is not always the answer

## Why This Exists

Fine-tuning changes model behavior.

That can improve task fit, but it can also overfit, regress general behavior, leak data, or waste money if the problem was actually routing, prompting, retrieval, caching, or serving.

AOIS needs an adaptation decision process before any training job exists.

## AOIS Connection

The AOIS path is now:

`serving and caching -> adaptation decision -> quantization and memory economics`

`v15` teaches when changing model behavior may be justified and how eval gates protect the system.

## Learning Goals

By the end of this version you should be able to:

- explain no-tuning baseline
- explain LoRA-style adaptation at a high level
- explain why full fine-tuning is a heavier path
- explain dataset card requirements
- explain train/validation/holdout split
- explain regression evals
- explain overfit checks
- run a local base-versus-adapted eval simulation
- explain why live training is gated

## Prerequisites

You should have completed:

- `v3` eval baseline
- `v14.5` performance and caching

Required checks:

```bash
python3 -m py_compile examples/validate_fine_tuning_plan.py examples/simulate_adaptation_eval.py
python3 examples/validate_fine_tuning_plan.py
python3 examples/simulate_adaptation_eval.py
```

## Core Concepts

## No-Tuning Baseline

The baseline shows current behavior before adaptation.

Do not train until the baseline is measured.

## Prompt Or Routing Adjustment

Some issues can be fixed by routing, prompts, retrieval, caching, or policy changes.

Try lower-cost changes before weight updates.

## LoRA-Style Adaptation

LoRA-style adaptation is a parameter-efficient tuning path.

In this lesson it is only a placeholder. No model is trained.

## Full Fine-Tuning

Full fine-tuning changes more model weights and carries higher cost and risk.

## Dataset Card

A dataset card documents source, license, intended use, risks, version, and quality.

## Holdout Eval

Holdout eval protects against overfitting to training and validation examples.

## Regression Eval

Regression eval checks that adaptation did not break existing behavior.

## Build

Inspect:

```bash
sed -n '1,260p' inference/aois-p/fine-tuning-adaptation.plan.json
sed -n '1,280p' examples/validate_fine_tuning_plan.py
sed -n '1,220p' examples/simulate_adaptation_eval.py
```

Compile:

```bash
python3 -m py_compile examples/validate_fine_tuning_plan.py examples/simulate_adaptation_eval.py
```

Validate:

```bash
python3 examples/validate_fine_tuning_plan.py
```

Simulate:

```bash
python3 examples/simulate_adaptation_eval.py
```

Expected validation:

```json
{
  "training_job_started": false,
  "dataset_uploaded": false,
  "model_downloaded": false,
  "gpu_runtime_started": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the plan and simulator:

1. Which options do not require training?
2. Which options require training?
3. Which field proves no dataset was uploaded?
4. Which field proves no training job started?
5. What is the simulator recommendation?
6. Why does it recommend not training yet?

Answer key:

1. `no_tuning_baseline` and `prompt_or_routing_adjustment`
2. `lora_style_placeholder` and `full_fine_tune_placeholder`
3. `dataset_uploaded=false`
4. `training_job_started=false`
5. `do_not_train_until_regressions_are_resolved`
6. the adapted candidate introduces a regression

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Start Training Too Early

Set:

```json
"training_job_started": true
```

Expected risk:

- adaptation work begins before dataset, eval, budget, and rollback controls exist

### Option B - Remove Holdout Eval

Set:

```json
"holdout_eval_required": false
```

Expected risk:

- the adapted candidate may overfit without being caught

### Option C - Remove Regression Eval

Set:

```json
"regression_eval_required": false
```

Expected risk:

- adaptation may improve one case while breaking existing behavior

## Testing

The version passes when:

1. both scripts compile
2. validator returns `status=pass`
3. simulator returns `status=pass`
4. training job remains false
5. dataset upload remains false
6. model download remains false
7. live training approval remains false
8. dataset and eval controls remain true

## Common Mistakes

- treating fine-tuning as the first fix
- training without a baseline
- using contaminated eval data
- skipping holdout evaluation
- ignoring regressions
- forgetting data license and PII review
- training when routing or caching would solve the problem

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_fine_tuning_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore training/runtime flags to `false`
- restore adaptation options
- restore dataset controls
- restore eval controls
- restore limits to zero
- restore required live checks

## Benchmark

Measure:

- validator compile result
- validator status
- simulator status
- base score
- adapted candidate score
- regression count
- training job status
- dataset upload status
- repo disk footprint
- memory snapshot

## Architecture Defense

Why not train immediately?

Because adaptation changes behavior and can create regressions.

Why require dataset controls?

Because training data defines what the model learns and what risk it carries.

Why require regression eval?

Because improving one capability is not acceptable if existing AOIS behavior breaks.

## 4-Layer Tool Drill

Tool: LoRA-style adaptation

1. Plain English
It adapts model behavior without updating all model weights.

2. System Role
It can improve domain fit with lower training cost than full fine-tuning.

3. Minimal Technical Definition
It is a parameter-efficient adaptation approach that trains a smaller set of additional parameters.

4. Hands-on Proof
The simulator compares base and adapted-candidate eval results without training.

## 4-Level System Explanation Drill

1. Simple English
AOIS evaluates adaptation before training.

2. Practical Explanation
I can compare baseline and adapted-candidate behavior and detect regressions.

3. Technical Explanation
`v15` adds a fine-tuning plan, validator, and no-training eval simulator.

4. Engineer-Level Explanation
AOIS now gates live adaptation behind dataset cards, PII and license review, data versioning, train/validation/holdout split, baseline eval, adapted eval, regression eval, quality gates, cost budget, rollback, and primary-project separation.

## Failure Story

Representative failure:

- Symptom: adapted model handles GPU incidents better but misclassifies ordinary operator requests
- Root cause: adaptation improved a narrow domain case but skipped regression evaluation
- Fix: reject the candidate, expand eval coverage, and resolve regressions before training
- Prevention: require baseline, adapted, holdout, and regression evals before live training
- What this taught me: adaptation is not improvement unless regressions are controlled

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v15` solve in AOIS?
2. What is a no-tuning baseline?
3. Why try prompt or routing adjustment before training?
4. What is LoRA-style adaptation?
5. Why is full fine-tuning heavier?
6. What is a dataset card?
7. Why is holdout eval required?
8. Why is regression eval required?
9. Why does the simulator recommend not training yet?
10. Explain LoRA-style adaptation using the 4-layer tool rule.
11. Explain `v15` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v15` solve in AOIS?

It teaches how to decide whether adaptation is justified before training.

2. What is a no-tuning baseline?

The measured behavior of the current system before adaptation.

3. Why try prompt or routing adjustment before training?

They are lower-cost and lower-risk than changing model weights.

4. What is LoRA-style adaptation?

A parameter-efficient approach to adapting model behavior with fewer trained parameters.

5. Why is full fine-tuning heavier?

It changes more weights and usually requires more data, compute, cost, and risk control.

6. What is a dataset card?

A document describing dataset source, license, intended use, quality, risks, and version.

7. Why is holdout eval required?

It catches overfitting beyond training and validation examples.

8. Why is regression eval required?

It checks that adaptation did not break existing behavior.

9. Why does the simulator recommend not training yet?

The adapted candidate introduces a regression.

10. Explain LoRA-style adaptation using the 4-layer tool rule.

- Plain English: it adapts behavior without updating all weights.
- System Role: it improves domain fit with lower training cost than full fine-tuning.
- Minimal Technical Definition: it trains a smaller set of additional parameters.
- Hands-on Proof: the simulator compares base and adapted-candidate eval results without training.

11. Explain `v15` using the 4-level system explanation rule.

- Simple English: AOIS evaluates adaptation before training.
- Practical explanation: I can compare baseline and adapted-candidate behavior.
- Technical explanation: `v15` adds an adaptation plan, validator, and no-training eval simulator.
- Engineer-level explanation: AOIS gates training behind dataset, privacy, license, split, eval, regression, quality, budget, rollback, and primary-separation controls.

## Connection Forward

`v15` defines adaptation decision discipline.

`v15.5` moves to quantization and memory economics, where AOIS learns what is gained and lost when reducing model footprint.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v15 Introduction](introduction.md)
- Next: [v15 Lab](lab.md)
<!-- AOIS-NAV-END -->
