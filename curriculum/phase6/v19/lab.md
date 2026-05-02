# v19 Lab

Authoring status: authored

## Build Lab

Compile and run the local-only chaos validator and simulator:

```bash
python3 -m py_compile examples/validate_chaos_engineering_plan.py examples/simulate_chaos_game_day.py
python3 examples/validate_chaos_engineering_plan.py
python3 examples/simulate_chaos_game_day.py
```

Expected validator result:

- `chaos_runtime_started: false`
- `fault_injection_executed: false`
- `load_test_started: false`
- `network_fault_started: false`
- `cpu_stress_started: false`
- `memory_stress_started: false`
- `pod_delete_executed: false`
- `agent_runtime_started: false`
- `provider_call_made: false`
- `status: pass`

Expected simulator result:

- API latency game day is tabletop-only.
- Stream lag game day is tabletop-only.
- Agent bad-recommendation game day is blocked.
- No live failure is injected.

## Ops Lab

Answer from the plan:

1. Which experiments are defined?
2. Which guardrails protect primary AOIS?
3. Which fields prove no memory or CPU stress occurred?
4. Which experiment has agent-specific risk?
5. Which live checks are required before real chaos?
6. What is the abort condition for each experiment?

## Break Lab

Use a scratch copy or reversible local edit only.

Break 1: set `memory_stress_started` to `true`.

Expected result: the validator fails because no stress tool may run in v19.

Break 2: remove `primary_aois_protection_required`.

Expected result: the validator fails because the primary project must be
protected.

Break 3: set an experiment to `approved_for_live_execution=true`.

Expected result: the validator fails because v19 is tabletop-only.

## Explanation Lab

Explain the chaos design flow:

1. Confirm steady state.
2. Write a hypothesis.
3. Define blast radius.
4. Define SLO and agent guardrails.
5. Define abort conditions.
6. Define rollback.
7. Assign game-day roles.
8. Run tabletop simulation.
9. Review what was learned.

## Defense Lab

Defend these decisions:

1. No live fault injection runs because there is no approved blast radius.
2. The primary AOIS project is excluded because it has priority on the server.
3. SLO budget is checked before chaos because exhausted budgets mean no
   reliability margin.
4. Agent chaos is included because AI failure can be quality or safety failure,
   not just service outage.
5. A blocked experiment is a valid success when guardrails detect unsafe
   conditions.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19 - Chaos Engineering Without Fault Injection](notes.md)
- Next: [v19 Runbook](runbook.md)
<!-- AOIS-NAV-END -->
