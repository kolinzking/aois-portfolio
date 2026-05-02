# v33 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_adversarial_red_teaming_plan.py examples/simulate_adversarial_red_teaming.py
python3 examples/validate_adversarial_red_teaming_plan.py
python3 examples/simulate_adversarial_red_teaming.py
```

Expected validator result:

```json
{
  "missing": [],
  "mode": "adversarial_red_teaming_plan_no_runtime",
  "namespace": "aois-p",
  "plan": "frontier/aois-p/adversarial-red-teaming.plan.json",
  "status": "pass"
}
```

Expected simulator summary:

```json
{
  "passed_cases": 25,
  "score": 1.0,
  "status": "pass",
  "total_cases": 25
}
```

## Interpretation

The benchmark covers safe sanitized recording, authorization blocks, scope
blocks, live-target blocks, unsafe-payload blocks, policy blocks, tool
overreach blocks, data-boundary blocks, telemetry holds, evidence holds,
mitigation holds, regression requirements, and escalation for prompt injection,
indirect injection, system prompt leakage, sensitive disclosure, poisoning,
excessive agency, output handling, unbounded consumption, edge cache poisoning,
fallback abuse, and policy confusion.

v33 passes only when validator status is `pass`, simulator status is `pass`, 25
of 25 cases pass, score is `1.0`, runtime boundary flags remain false, and no
placeholder marker remains in the v33 lesson pack.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v33 Failure Story](failure-story.md)
- Next: [v33 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
