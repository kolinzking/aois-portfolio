# v34 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_governance_computer_use_plan.py examples/simulate_governance_computer_use.py
python3 examples/validate_governance_computer_use_plan.py
python3 examples/simulate_governance_computer_use.py
```

Expected validator result:

```json
{
  "missing": [],
  "mode": "governance_computer_use_plan_no_runtime",
  "namespace": "aois-p",
  "plan": "frontier/aois-p/governance-computer-use.plan.json",
  "status": "pass"
}
```

Expected simulator summary:

```json
{
  "passed_cases": 21,
  "score": 1.0,
  "status": "pass",
  "total_cases": 21
}
```

## Interpretation

The benchmark covers observe-only allow, draft-only allow, synthetic plan
recording, manual route, governance block, environment block, live-target block,
approval hold, credential block, privacy block, high-impact block, transaction
block, safety-check hold, preview hold, budget block, stop-control block,
rollback block, audit hold, red-team block, release block, and policy block.

v34 passes only when validator status is `pass`, simulator status is `pass`, 21
of 21 cases pass, score is `1.0`, runtime boundary flags remain false, and no
placeholder marker remains in the v34 lesson pack.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v34 Failure Story](failure-story.md)
- Next: [v34 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
