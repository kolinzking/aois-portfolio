# v15 Lab

Authoring status: authored

## Build Lab

Run:

```bash
python3 -m py_compile examples/validate_fine_tuning_plan.py examples/simulate_adaptation_eval.py
python3 examples/validate_fine_tuning_plan.py
python3 examples/simulate_adaptation_eval.py
```

## Ops Lab

Answer:

1. Did a training job start?
2. Was a dataset uploaded?
3. What is the base score?
4. What is the adapted candidate score?
5. How many regressions exist?

Answer key:

1. no
2. no
3. `0.75`
4. `0.75`
5. `1`

## Break Lab

Use a scratch copy only.

Break 1: set `max_training_jobs_for_lesson` to `1`.

Expected result: validation fails because no training job is approved.

Break 2: remove `pii_review_required`.

Expected result: validation fails because training data needs privacy review.

Break 3: remove `rollback_plan_required`.

Expected result: validation fails because adapted behavior needs rollback.

## Explanation Lab

Explain:

1. Why the adapted candidate is not accepted.
2. Why data controls are required before training.
3. Why regression eval is mandatory.
4. Why prompt/routing changes may be better than tuning.
5. Why fine-tuning is not automatically frontier engineering.

## Defense Lab

Defend this decision:

AOIS should not train until dataset card, privacy review, license review, data versioning, split strategy, baseline eval, quality gate, cost budget, training approval, rollback, and primary AOIS separation exist.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v15 - Fine-Tuning And Adaptation Without Training](notes.md)
- Next: [v15 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
