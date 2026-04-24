# v10.5 Benchmark

Authoring status: authored

## Measurements

Record these measurements after running the validator:

- validator compile result
- validator status
- selected runtime option
- `cloud_agent_created`
- `credentials_used`
- repo disk footprint
- memory snapshot

Commands:

```bash
python3 -m py_compile examples/validate_managed_agent_plan.py
python3 examples/validate_managed_agent_plan.py
du -sh .
free -h
```

## Interpretation

A passing benchmark proves only this:

- the tradeoff plan is internally consistent
- the current choice remains AOIS-owned runtime
- the lesson did not require cloud credentials
- the lesson did not create a cloud agent

It does not prove that a real managed-agent service is production-ready for AOIS.

Production readiness would require provider-specific docs review, live-service cost analysis, IAM/security design, tool permission policy, observability review, eval baseline, and rollback rehearsal.
