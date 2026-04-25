# v19.5 Summary Notes

Authoring status: authored

v19.5 adds AI failure governance to AOIS.

Key points:

- AI can fail while the API still succeeds.
- Unsupported confidence is a failure mode.
- Evidence is required before root-cause claims and operational
  recommendations.
- Secret-bearing input blocks provider use.
- Destructive action requires human approval.
- Tool access defaults to deny.
- Primary AOIS resources remain excluded from portfolio practice.
- Governance decisions are allowed, reviewed, blocked, or sent to fallback.
- Local policy simulation comes before live enforcement.

Artifacts:

- `release-safety/aois-p/ai-failure-governance.plan.json`
- `examples/validate_ai_failure_governance_plan.py`
- `examples/simulate_ai_failure_governance.py`

The version prepares AOIS for Phase 7 by making tool-using agents subject to
policy before they gain real capabilities.
