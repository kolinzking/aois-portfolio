# v26 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_dashboard_visibility_plan.py examples/simulate_dashboard_visibility.py
python3 examples/validate_dashboard_visibility_plan.py
python3 examples/simulate_dashboard_visibility.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- API, frontend, browser, stream, network, and provider flags

## Interpretation

Pass means:

- all dashboard panels are defined
- event ordering and dedupe fields exist
- every supported event type is listed
- all visibility decisions have cases
- stale state, empty state, connection loss, redaction, and accessibility gates are modeled
- no live frontend, stream, browser, provider, or network runtime is enabled

Fail means the dashboard visibility contract is incomplete. Fix the plan or
simulator before adding identity-aware access in v27.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v26 Failure Story](failure-story.md)
- Next: [v26 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
