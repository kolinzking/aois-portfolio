# v19 Contents

Authoring status: authored

Topic: Chaos engineering for AI infrastructure

Safety mode: local plan and tabletop simulation only. This version does not
inject faults, run load tests, create network faults, stress CPU or memory,
delete pods, start agent runtime, call providers, mutate cloud resources, or
start persistent services.

## Start Here

1. Read [02-introduction.md](02-introduction.md) to understand why chaos engineering
   follows incident response.
2. Read [03-notes.md](03-notes.md) for the full steady-state, hypothesis,
   blast-radius, abort, rollback, and game-day model.
3. Inspect `chaos/aois-p/chaos-engineering.plan.json`.
4. Run:

```bash
python3 -m py_compile examples/validate_chaos_engineering_plan.py examples/simulate_chaos_game_day.py
python3 examples/validate_chaos_engineering_plan.py
python3 examples/simulate_chaos_game_day.py
```

Expected result: both scripts pass while all runtime and fault-injection flags
remain false.

## Topic Jumps

- Steady state, hypothesis, and blast radius: [03-notes.md](03-notes.md)
- Hands-on validation and break exercises: [04-lab.md](04-lab.md)
- Recovery procedure: [05-runbook.md](05-runbook.md)
- Measurement checklist: [07-benchmark.md](07-benchmark.md)
- Unsafe memory-stress failure story: [06-failure-story.md](06-failure-story.md)
- Transition to AI failure governance: [10-next-version-bridge.md](10-next-version-bridge.md)

## Self-Paced Path

1. Explain why chaos engineering is not random breakage.
2. Identify the v19 experiments and their guardrails.
3. Run the validator and prove no fault injection occurred.
4. Run the simulator and identify which experiment is blocked.
5. Explain why the primary AOIS workload is excluded.
6. Break the plan in a scratch edit and use validator output to explain the
   risk.
7. Answer the mastery checkpoint in [03-notes.md](03-notes.md).
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19 Start Here](00-start-here.md)
- Next: [v19 Introduction](02-introduction.md)
<!-- AOIS-NAV-END -->
