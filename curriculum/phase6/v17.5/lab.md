# v17.5 Lab

Authoring status: authored

## Build Lab

Compile and run the local-only SLO validator and simulator:

```bash
python3 -m py_compile examples/validate_service_agent_slo_plan.py examples/simulate_slo_error_budget.py
python3 examples/validate_service_agent_slo_plan.py
python3 examples/simulate_slo_error_budget.py
```

Expected validator result:

- `slo_runtime_started: false`
- `metrics_backend_started: false`
- `alerting_runtime_started: false`
- `dashboard_runtime_started: false`
- `agent_runtime_started: false`
- `provider_call_made: false`
- `status: pass`

Expected simulator result:

- API budget remains positive.
- Stream consumer budget remains positive but low.
- Incident agent budget is exhausted.
- Recommended action freezes risky changes and routes affected work to human
  review.

## Ops Lab

Answer from the plan:

1. Which SLO protects API request success?
2. Which SLO protects event freshness?
3. Which SLO protects agent recommendation quality?
4. Which controls stop destructive agent action from continuing unchecked?
5. Which policy connects SLO failure to release or automation decisions?
6. Which fields prove this lesson did not start monitoring or agent runtime?

## Break Lab

Use a scratch copy or reversible local edit only.

Break 1: set `metrics_backend_started` to `true`.

Expected result: the validator fails because v17.5 is not a live monitoring
deployment.

Break 2: remove `human_review_required_for_destructive_action`.

Expected result: the validator fails because destructive agent actions need a
human review gate.

Break 3: set `max_persistent_storage_mb` to `500`.

Expected result: the validator fails because this lesson is not allowed to
create persistent monitoring storage.

## Explanation Lab

Explain the v17.5 reliability flow:

1. AOIS defines an SLI.
2. AOIS sets an SLO target over a time window.
3. AOIS calculates the allowed failure budget.
4. AOIS measures bad events against that budget.
5. Burn rate decides urgency.
6. Exhausted budgets change operational policy.
7. Agent quality and safety failures route risky work to human review.

## Defense Lab

Defend these decisions:

1. No live monitoring runtime is started because the policy can be learned
   without spending memory or disk.
2. Agent SLOs include quality and safety because HTTP success is not enough.
3. Burn rate alerts are required because monthly SLO misses are discovered too
   late.
4. Error budgets must affect change policy or they become vanity metrics.
5. Human review is mandatory when an agent budget is exhausted or action is
   destructive.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v17.5 - Service And Agent SLOs Without Runtime](notes.md)
- Next: [v17.5 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
