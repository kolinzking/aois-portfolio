# v19 Summary Notes

Authoring status: authored

## What Was Built

A local-only chaos engineering lesson for AOIS:

- `chaos/aois-p/chaos-engineering.plan.json`
- `examples/validate_chaos_engineering_plan.py`
- `examples/simulate_chaos_game_day.py`
- authored v19 notes, lab, runbook, benchmark, failure story, and bridge

No fault injection, load test, network fault, CPU stress, memory stress, pod
delete, agent runtime, provider call, cloud call, install, or persistent runtime
was started.

## What Was Learned

You learned that chaos engineering is disciplined experimentation, not random
breakage.

Key ideas:

- steady state comes first
- experiments need hypotheses
- blast radius must be explicit
- abort conditions must exist before the experiment starts
- SLO budget controls whether extra risk is acceptable
- primary AOIS is excluded from curriculum chaos
- AI agents need chaos scenarios for quality, safety, evidence, and tool use

## Core Limitation Or Tradeoff

v19 does not prove live fault-injection behavior. That is intentional. The
tradeoff is lower realism in exchange for zero runtime footprint and zero risk
to the shared server.

Live chaos should only happen after explicit approval, blast-radius review,
resource headroom review, SLO budget review, communication plan, abort
conditions, rollback plan, and primary-project protection.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19 Benchmark](benchmark.md)
- Next: [v19 Looking Forward](looking-forward.md)
<!-- AOIS-NAV-END -->
