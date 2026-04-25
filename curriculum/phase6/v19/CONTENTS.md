# v19 Contents

Authoring status: authored

Topic: Chaos engineering for AI infrastructure

Safety mode: local plan and tabletop simulation only. This version does not
inject faults, run load tests, create network faults, stress CPU or memory,
delete pods, start agent runtime, call providers, mutate cloud resources, or
start persistent services.

## Start Here

1. Read [introduction.md](introduction.md) to understand why chaos engineering
   follows incident response.
2. Read [notes.md](notes.md) for the full steady-state, hypothesis,
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

- Steady state, hypothesis, and blast radius: [notes.md](notes.md)
- Hands-on validation and break exercises: [lab.md](lab.md)
- Recovery procedure: [runbook.md](runbook.md)
- Measurement checklist: [benchmark.md](benchmark.md)
- Unsafe memory-stress failure story: [failure-story.md](failure-story.md)
- Transition to AI failure governance: [next-version-bridge.md](next-version-bridge.md)

## Self-Paced Path

1. Explain why chaos engineering is not random breakage.
2. Identify the v19 experiments and their guardrails.
3. Run the validator and prove no fault injection occurred.
4. Run the simulator and identify which experiment is blocked.
5. Explain why the primary AOIS workload is excluded.
6. Break the plan in a scratch edit and use validator output to explain the
   risk.
7. Answer the mastery checkpoint in [notes.md](notes.md).
