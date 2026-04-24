# v15.5 - Quantization And Memory Economics Without Runtime

Estimated time: 8-10 focused hours

Authoring status: authored

Resource posture: quantization plan and simulation only, no quantization job, no model download, no GPU runtime, no inference runtime

## What This Builds

This version builds a quantization and memory economics plan:

- `inference/aois-p/quantization-memory.plan.json`
- `examples/validate_quantization_plan.py`
- `examples/simulate_quantization_tradeoffs.py`

It teaches:

- FP16 baseline
- INT8 placeholder
- INT4 placeholder
- memory reduction
- speed and quality tradeoffs
- calibration data review
- task regression eval
- fallback precision planning

## Why This Exists

Model deployment is constrained by memory.

Quantization can make deployment more realistic, but it trades precision for footprint and sometimes quality.

AOIS needs to reason about what is gained and lost before quantizing or serving a model.

## AOIS Connection

The AOIS path is now:

`GPU serving -> performance caching -> adaptation decision -> quantization economics`

`v15.5` closes Phase 5 by teaching model footprint tradeoffs.

## Learning Goals

By the end of this version you should be able to:

- explain quantization
- explain precision tradeoffs
- compare FP16, INT8, and INT4 placeholders
- explain memory reduction versus quality delta
- explain calibration data review
- explain task regression eval
- explain why fallback precision is required
- validate a quantization plan locally without running quantization

## Prerequisites

You should have completed:

- `v13` GPU inference service planning
- `v14` high-throughput serving
- `v15` fine-tuning and adaptation

Required checks:

```bash
python3 -m py_compile examples/validate_quantization_plan.py examples/simulate_quantization_tradeoffs.py
python3 examples/validate_quantization_plan.py
python3 examples/simulate_quantization_tradeoffs.py
```

## Core Concepts

## Quantization

Quantization reduces the numeric precision used to represent model weights or activations.

The goal is lower memory footprint and sometimes faster inference.

## FP16 Baseline

FP16 is the baseline in this lesson.

It has higher memory use but better simulated quality.

## INT8 And INT4

INT8 and INT4 placeholders represent lower-precision options.

They reduce memory but may reduce output quality.

## Memory Economics

Memory economics asks what model size can fit on available hardware and what quality is lost by fitting it.

## Calibration Data

Some quantization methods need calibration data.

That data must be reviewed for representativeness and safety.

## Fallback Precision

Fallback precision means keeping a safer precision path available if lower precision fails quality gates.

## Build

Inspect:

```bash
sed -n '1,260p' inference/aois-p/quantization-memory.plan.json
sed -n '1,280p' examples/validate_quantization_plan.py
sed -n '1,220p' examples/simulate_quantization_tradeoffs.py
```

Compile:

```bash
python3 -m py_compile examples/validate_quantization_plan.py examples/simulate_quantization_tradeoffs.py
```

Validate:

```bash
python3 examples/validate_quantization_plan.py
```

Simulate:

```bash
python3 examples/simulate_quantization_tradeoffs.py
```

Expected validation:

```json
{
  "quantization_job_started": false,
  "model_downloaded": false,
  "gpu_runtime_started": false,
  "inference_runtime_started": false,
  "namespace": "aois-p",
  "status": "pass"
}
```

## Ops Lab

Answer from the simulator:

1. Which option is the baseline?
2. Which option has the lowest memory footprint?
3. Which option has the best simulated quality score?
4. Which metric shows quality loss?
5. Which field proves no quantization job started?

Answer key:

1. `fp16-baseline`
2. `int4-placeholder`
3. `fp16-baseline`
4. `quality_delta_vs_fp16`
5. `quantization_job_started=false`

## Break Lab

Do not skip this.

Use a scratch copy only.

### Option A - Start Quantization Too Early

Set:

```json
"quantization_job_started": true
```

Expected risk:

- model artifact work begins before quality and fallback controls exist

### Option B - Remove Quality Eval

Set:

```json
"quality_eval_required": false
```

Expected risk:

- lower precision may be accepted without proving output quality

### Option C - Remove Fallback Precision

Set:

```json
"fallback_precision_required": false
```

Expected risk:

- AOIS has no safe path if INT8/INT4 quality fails

## Testing

The version passes when:

1. both scripts compile
2. validator returns `status=pass`
3. simulator returns `status=pass`
4. quantization job remains false
5. model download remains false
6. runtime flags remain false
7. precision options remain present
8. quality, memory, latency, throughput, regression, fallback, and rollback controls remain true

## Common Mistakes

- treating quantization as free speed
- measuring memory but not quality
- ignoring task regression
- skipping calibration data review
- accepting INT4 without fallback
- downloading model artifacts before approval

## Troubleshooting

If validation fails:

```bash
python3 examples/validate_quantization_plan.py
```

Read `missing`, inspect the plan, and restore required fields.

Common fixes:

- restore runtime/job flags to `false`
- restore precision options
- restore controls
- restore limits to zero
- restore live checks

## Benchmark

Measure:

- validator status
- simulator status
- memory by option
- speed index by option
- quality score by option
- memory reduction versus FP16
- quality delta versus FP16
- repo disk footprint
- memory snapshot

## Architecture Defense

Why quantize?

To reduce memory footprint and potentially improve deployment economics.

Why not always use the smallest precision?

Because quality can degrade and task regressions can appear.

Why require fallback precision?

Because lower precision must be reversible if it fails quality gates.

## 4-Layer Tool Drill

Tool: quantization

1. Plain English
It stores model numbers with fewer bits.

2. System Role
It can reduce memory footprint and deployment cost.

3. Minimal Technical Definition
It converts model numerical representation to lower precision while trying to preserve acceptable task quality.

4. Hands-on Proof
The simulator compares memory reduction and quality delta without quantizing a model.

## 4-Level System Explanation Drill

1. Simple English
AOIS compares precision tradeoffs without changing a model.

2. Practical Explanation
I can compare FP16, INT8, and INT4 memory, speed, and quality tradeoffs.

3. Technical Explanation
`v15.5` adds a quantization plan, validator, and local tradeoff simulator.

4. Engineer-Level Explanation
AOIS now gates quantization behind model approval, method review, calibration review, quality eval, task regression eval, memory and latency benchmarks, fallback precision, rollback, and primary-project separation.

## Failure Story

Representative failure:

- Symptom: INT4 deployment fits memory but gives worse incident recommendations
- Root cause: quality and task regression evals were skipped
- Fix: roll back to FP16 or INT8 and rerun evals
- Prevention: validate quantization controls before artifact creation
- What this taught me: smaller is not automatically better

## Mastery Checkpoint

Do not move on until you can answer:

1. What problem does `v15.5` solve in AOIS?
2. What is quantization?
3. Why is FP16 the baseline?
4. What is gained by INT8 or INT4?
5. What can be lost by INT8 or INT4?
6. Why is calibration review required?
7. Why is task regression eval required?
8. Why is fallback precision required?
9. Why is no quantization job started?
10. Explain quantization using the 4-layer tool rule.
11. Explain `v15.5` using the 4-level system explanation rule.

## Mastery Checkpoint Answer Key

Use this after attempting the answers yourself.
Do not read it first if you are testing recall.

1. What problem does `v15.5` solve in AOIS?

It teaches model footprint and precision tradeoffs before quantization.

2. What is quantization?

Representing model numbers with fewer bits.

3. Why is FP16 the baseline?

It provides a higher-quality reference for comparing lower precision options.

4. What is gained by INT8 or INT4?

Lower memory footprint and possibly faster serving.

5. What can be lost by INT8 or INT4?

Output quality and task reliability.

6. Why is calibration review required?

Calibration data can shape quantization behavior and must represent the task safely.

7. Why is task regression eval required?

It catches quality losses on AOIS tasks.

8. Why is fallback precision required?

It provides a safe rollback path if low precision fails.

9. Why is no quantization job started?

This lesson is plan and simulation only; live artifact work needs approval.

10. Explain quantization using the 4-layer tool rule.

- Plain English: it stores model numbers with fewer bits.
- System Role: it reduces memory footprint and deployment cost.
- Minimal Technical Definition: it lowers numerical precision while trying to preserve quality.
- Hands-on Proof: the simulator compares memory and quality tradeoffs without quantizing.

11. Explain `v15.5` using the 4-level system explanation rule.

- Simple English: AOIS compares precision tradeoffs without changing a model.
- Practical explanation: I can compare memory reduction, speed, and quality loss.
- Technical explanation: `v15.5` adds a quantization plan, validator, and simulator.
- Engineer-level explanation: AOIS gates quantization behind method review, calibration review, quality eval, regression eval, memory and latency benchmarks, fallback precision, rollback, and primary-project separation.

## Connection Forward

`v15.5` closes Phase 5.

Phase 6 moves into observability, streaming, and reliability so AOIS can see and test the behavior of the systems it has planned.
