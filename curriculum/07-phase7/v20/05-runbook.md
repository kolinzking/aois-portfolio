# v20 Runbook

Authoring status: authored

## Purpose

Recover the v20 local tool-using responder lesson when validation, simulation,
or explanation gets stuck.

This runbook does not start a live agent, execute tools, or call a provider.

## Primary Checks

Run:

```bash
python3 -m py_compile examples/validate_tool_using_responder_plan.py examples/simulate_tool_using_responder.py
python3 examples/validate_tool_using_responder_plan.py
python3 examples/simulate_tool_using_responder.py
```

Expected:

```text
status: pass
agent_runtime_started: false
tool_calls_executed: false
provider_call_made: false
```

## Recovery Steps

If validation fails:

1. Read the `missing` list.
2. Restore the named field in `agentic/aois-p/tool-using-responder.plan.json`.
3. Confirm all runtime and spend limits remain zero.
4. Re-run the validator.

If simulation fails:

1. Find the case with `passed: false`.
2. Compare `decision` to `expected_decision`.
3. Check whether the case has a secret, mutating tool, invalid schema, or
   incomplete evidence.
4. Restore the expected case fields.
5. Re-run the simulator.

If a mutating tool is allowed:

1. Add it to `blocked_tools_without_human_approval`.
2. Confirm `human_approval_for_mutation` is true.
3. Confirm `max_mutating_tool_calls_without_approval` is `0`.
4. Re-run validation and simulation.

If a learner wants to run live tools:

Stop. v20 is not the live execution step. The required live checks are listed
under `required_before_live_agent_execution`.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](../../READING-ORDER.md)
- Previous: [v20 Lab](04-lab.md)
- Next: [v20 Failure Story](06-failure-story.md)
<!-- AOIS-NAV-END -->
