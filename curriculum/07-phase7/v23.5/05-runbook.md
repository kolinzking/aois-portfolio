# v23.5 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to evaluate whether connected agent behavior
is safe and correct across routing, registry, workflow, and orchestration
layers.

## Primary Checks

1. Confirm the evaluation is scoped to `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm every case has case id, incident id, and trace id.
4. Confirm case types cover happy path, approval, safety block, budget guard, loop guard, and timeout.
5. Confirm expected and observed outputs exist.
6. Confirm metric weights sum to `1.0`.
7. Confirm critical metrics include registry and safety gate accuracy.
8. Confirm thresholds require full pass for this local corpus.
9. Confirm no provider, tool, or external eval service is called.
10. Confirm source notes are current.

## Recovery Steps

Run:

```bash
python3 examples/validate_agent_evaluation_plan.py
python3 examples/simulate_agent_evaluation.py
```

Decision handling:

- `status: pass`: the local connected behavior matches the golden cases.
- `missing` is non-empty: repair the evaluation plan shape.
- `overall_score < 1.0`: inspect failed metric results.
- `safety_score < 1.0`: block promotion and inspect safety cases.
- `critical_pass_rate < 1.0`: block promotion and repair critical behavior.

Escalate to a human operator if:

- any safety block case passes incorrectly
- approval waits are not enforced
- budget reserve is not enforced
- metric weights change
- dataset coverage changes
- external eval service flags are enabled
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v23.5 Lab](04-lab.md)
- Next: [v23.5 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
