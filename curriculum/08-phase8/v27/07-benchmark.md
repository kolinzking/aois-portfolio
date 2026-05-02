# v27 Benchmark

Authoring status: authored

## Measurements

Run:

```bash
python3 -m py_compile examples/validate_policy_aware_access_plan.py examples/simulate_policy_aware_access.py
python3 examples/validate_policy_aware_access_plan.py
python3 examples/simulate_policy_aware_access.py
```

Record:

- validator status
- simulator status
- passed cases
- total cases
- score
- auth, identity provider, token, session, API, frontend, policy, database, network, and provider flags

## Interpretation

Pass means:

- role catalog is complete
- resource catalog is complete
- permissions are explicit and non-wildcard
- every resource is tenant scoped
- policy order is deny-first
- every access decision has a case
- raw sensitive state is blocked
- self-approval is blocked
- cross-tenant access is denied unless the limited break-glass case applies
- access decisions are audited
- no live auth, policy, network, or provider runtime is enabled

Fail means the access contract is incomplete. Fix the plan or simulator before
moving into Phase 9 delivery and release controls.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v27 Failure Story](06-failure-story.md)
- Next: [v27 Summary Notes](08-summary-notes.md)
<!-- AOIS-NAV-END -->
