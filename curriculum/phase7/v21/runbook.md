# v21 Runbook

Authoring status: authored

## Purpose

Use this runbook when AOIS-P needs to decide whether a requested MCP tool should
be exposed to a selected agentic route, paused for approval, or blocked before
execution.

## Primary Checks

1. Confirm the case is in `aois-p`.
2. Confirm primary AOIS is excluded.
3. Confirm the v20.2 route decision is known.
4. Confirm the requested server label is trusted.
5. Confirm every requested tool is registered.
6. Confirm every tool has an owner.
7. Confirm input and output schema references exist.
8. Confirm side-effect level is classified.
9. Confirm the tool is allowed for the selected route.
10. Confirm sensitive reads require approval.
11. Confirm write and privileged tools are blocked by default.
12. Confirm audit event names exist.
13. Confirm MCP, registry runtime, tool execution, and provider flags are disabled.

## Recovery Steps

Run:

```bash
python3 examples/validate_governed_tool_registry_plan.py
python3 examples/simulate_governed_tool_registry.py
```

Decision handling:

- `allow_no_tool_route`: expose no tools and answer from existing evidence.
- `allow_read_only_tool_plan`: keep the bounded read-only tools in the plan only.
- `require_human_approval`: pause before any sensitive read is executed.
- `block_unregistered_tool`: reject the request and require registry review.
- `block_untrusted_server`: reject the server label before inspecting tool semantics.
- `block_side_effecting_tool`: block writes until live-remediation governance exists.
- `block_disabled_tool`: keep the tool unavailable.

Escalate to a human operator if:

- a tool has no owner
- a requested server is unknown
- a requested tool is not registered
- a sensitive tool lacks approval policy
- a write or privileged tool is requested
- any live execution flag is enabled
