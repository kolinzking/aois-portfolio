# v20.2 Introduction

Authoring status: authored

## What This Version Is About

v20.1 made agentic responder cost visible after a plan existed. v20.2 uses that
cost visibility earlier, before spend happens.

This version teaches AOIS-P to choose a route:

```text
incident -> evidence state -> confidence -> remaining budget -> route
```

The route can be a small no-tool answer, a bounded read-only evidence pass,
human budget review, a stop decision, or a high-severity full investigation.

## Why It Matters In AOIS

Agentic systems should not spend just because a next step is possible.

They need to ask:

- is the evidence already complete
- is confidence high enough to skip another tool
- does the route fit the remaining budget
- is the incident severe enough to justify a larger route
- should a human review the branch before expensive spend
- is the cost ledger complete enough to trust

## How To Use This Version

Use the local plan and deterministic scripts:

```bash
python3 -m py_compile examples/validate_budget_aware_routing_plan.py examples/simulate_budget_aware_routing.py
python3 examples/validate_budget_aware_routing_plan.py
python3 examples/simulate_budget_aware_routing.py
```

No runtime starts, no tool executes, no provider is called, and no billing API is
called.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20.2 Contents](01-contents.md)
- Next: [v20.2 - Budget-Aware Routing](03-notes.md)
<!-- AOIS-NAV-END -->
