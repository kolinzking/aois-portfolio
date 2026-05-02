# v19.5 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 examples/validate_ai_failure_governance_plan.py
python3 examples/simulate_ai_failure_governance.py
```

Record:

- validator status
- simulator status
- passed policy cases
- total policy cases
- policy score
- runtime flags
- provider-call flag
- tool-call flag

Expected benchmark:

- validator status: `pass`
- simulator status: `pass`
- passed policy cases: `7`
- total policy cases: `7`
- policy score: `1.0`
- all runtime flags: `false`
- `tool_calls_executed`: `false`
- `provider_call_made`: `false`

## Interpretation

A score of `1.0` does not prove the policy is production-ready. It proves the
local governance model is internally consistent for the cases in this lesson.

The useful benchmark is not speed. The useful benchmark is whether the policy
correctly separates:

- allowed low-risk output
- uncertain output needing human review
- unsafe output that must be blocked
- invalid or degraded model output that must fall back

For live use, this benchmark would need broader cases, adversarial prompts,
tool-permission tests, audit-log retention checks, and incident-response
integration.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v19.5 Failure Story](failure-story.md)
- Next: [v19.5 Summary Notes](summarynotes.md)
<!-- AOIS-NAV-END -->
