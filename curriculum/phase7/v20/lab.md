# v20 Lab

Authoring status: authored

## Build Lab

Build the local responder evidence loop by inspecting:

```bash
sed -n '1,360p' agentic/aois-p/tool-using-responder.plan.json
sed -n '1,320p' examples/validate_tool_using_responder_plan.py
sed -n '1,260p' examples/simulate_tool_using_responder.py
```

Then run:

```bash
python3 -m py_compile examples/validate_tool_using_responder_plan.py examples/simulate_tool_using_responder.py
python3 examples/validate_tool_using_responder_plan.py
python3 examples/simulate_tool_using_responder.py
```

Expected result:

```text
status: pass
tool_calls_executed: false
```

## Ops Lab

Answer from simulator output:

1. Which case produces `answer_with_evidence`?
2. Which case produces `request_human_approval`?
3. Which planned step is not allowed without approval?
4. Which case produces `block_and_redact`?
5. Which case produces `fallback_to_runbook`?

Answer key:

1. `latency_spike_with_complete_evidence`.
2. `crashloop_with_pod_delete_request`.
3. `delete_pod`.
4. `secret_bearing_log_excerpt`.
5. `malformed_trace_tool_result`.

## Break Lab

Make one scratch edit:

```text
"tool_type": "mutating"
```

Use it on one allowed read-only tool, then run:

```bash
python3 examples/validate_tool_using_responder_plan.py
```

Expected symptom:

```text
tool_must_be_read_only
status: fail
```

Fix:

Restore `"tool_type": "read_only"` and re-run validation.

False conclusion prevented:

```text
It is safe because the tool is only part of a plan.
```

Correct conclusion:

```text
Even planned tools need accurate capability classification.
```

## Explanation Lab

Explain the system at four levels:

1. Plain English: AOIS chooses tools safely before using them.
2. System role: the responder turns incident symptoms into bounded evidence
   steps.
3. Minimal technical definition: a JSON plan plus validator and simulator for
   tool decisions.
4. Hands-on proof: validation and simulation pass with no tool execution.

## Defense Lab

Defend these choices:

- Local simulation instead of live tool execution.
- Read-only tools before mutating tools.
- Strict schemas for tool inputs and outputs.
- Human approval for destructive action.
- Fallback when tool output is malformed.
