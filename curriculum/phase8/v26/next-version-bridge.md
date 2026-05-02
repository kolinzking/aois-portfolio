# v26 Next Version Bridge

Authoring status: authored

## What This Version Unlocks

v26 gives AOIS-P a product-surface visibility contract:

- incident overview
- trace timeline
- route and registry panel
- workflow and orchestration panel
- autonomy and agent panel
- approval queue
- budget panel
- execution-boundary panel
- stale-state, empty-state, connection-loss, redaction, and accessibility behavior

## Why The Next Version Exists

v27 adds auth, tenancy, permissions, and policy-aware access.

Once AOIS-P has dashboard panels, the next risk is showing the wrong state to
the wrong user. Incidents, traces, approvals, budgets, agent state, and
execution-boundary decisions may have different viewers, approvers, and owners.

The bridge from v26 to v27 is:

```text
show operators what AOIS is doing -> control who may see and act on each state
```
