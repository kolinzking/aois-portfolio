# v20 Benchmark

Authoring status: authored

## Measurements

Record these values:

```text
validator_status = pass
simulator_status = pass
passed_cases = 5
total_cases = 5
score = 1.0
agent_runtime_started = false
tool_calls_executed = false
provider_call_made = false
```

Commands:

```bash
python3 examples/validate_tool_using_responder_plan.py
python3 examples/simulate_tool_using_responder.py
```

## Interpretation

A passing benchmark proves that the local responder plan is internally
consistent:

- read-only tools are allowlisted
- mutating tools are blocked without approval
- secret-bearing evidence blocks and redacts
- incomplete evidence gathers more evidence
- malformed tool output falls back
- no live agent or tool execution occurred

It does not prove production readiness. Live execution still needs real tool
integration tests, approval UX, audit storage, rollback, and provider/cost
controls.
