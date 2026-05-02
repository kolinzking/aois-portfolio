#!/usr/bin/env python3
"""Simulate Phase 7 v21 governed MCP tool registry decisions without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("agentic/aois-p/governed-tool-registry.plan.json")


def _tool_index(plan: dict[str, object]) -> dict[tuple[str, str], dict[str, object]]:
    return {
        (str(tool["server_label"]), str(tool["tool_name"])): tool
        for tool in plan["tool_catalog"]
    }


def _tool_summary(tool: dict[str, object]) -> dict[str, object]:
    return {
        "tool_name": tool["tool_name"],
        "server_label": tool["server_label"],
        "side_effect_level": tool["side_effect_level"],
        "approval_policy": tool["approval_policy"],
        "status": tool["status"],
        "audit_event": tool["audit_event"],
    }


def _decide(case: dict[str, object], plan: dict[str, object]) -> dict[str, object]:
    requested_tools = list(case["requested_tools"])
    requested_server = str(case["requested_server_label"])
    allowed_servers = {str(server) for server in plan["allowed_server_labels"]}
    index = _tool_index(plan)

    allowed_tools: list[str] = []
    approvals: list[str] = []
    blocks: list[str] = []
    inspected_tools: list[dict[str, object]] = []
    reasons: list[str] = []

    if not requested_tools:
        decision = "allow_no_tool_route"
        reasons.append("route_requests_no_tools")
    elif requested_server not in allowed_servers:
        decision = "block_untrusted_server"
        blocks.extend(str(tool) for tool in requested_tools)
        reasons.append("requested_server_label_is_not_trusted_for_aois_p")
    else:
        decision = "allow_read_only_tool_plan"
        for tool_name in requested_tools:
            key = (requested_server, str(tool_name))
            tool = index.get(key)
            if tool is None:
                decision = "block_unregistered_tool"
                blocks.append(str(tool_name))
                reasons.append(f"unregistered_tool:{tool_name}")
                break

            inspected_tools.append(_tool_summary(tool))
            status = str(tool["status"])
            side_effect = str(tool["side_effect_level"])
            route_id = str(case["route_id"])
            route_decision = str(case["route_decision"])

            if status == "disabled":
                decision = "block_disabled_tool"
                blocks.append(str(tool_name))
                reasons.append(f"disabled_tool:{tool_name}")
                break
            if side_effect in {"write_effect", "privileged_execution"}:
                decision = "block_side_effecting_tool"
                blocks.append(str(tool_name))
                reasons.append(f"side_effecting_tool_blocked_by_default:{tool_name}")
                break
            if route_id not in tool["allowed_routes"]:
                decision = "block_unregistered_tool"
                blocks.append(str(tool_name))
                reasons.append(f"tool_not_allowed_for_route:{tool_name}:{route_id}")
                break
            if route_decision not in tool["allowed_decisions"]:
                decision = "block_unregistered_tool"
                blocks.append(str(tool_name))
                reasons.append(f"tool_not_allowed_for_decision:{tool_name}:{route_decision}")
                break

            allowed_tools.append(str(tool_name))
            if tool["human_approval_required"] is True:
                approvals.append(str(tool_name))

        if decision == "allow_read_only_tool_plan" and approvals:
            decision = "require_human_approval"
            reasons.append("sensitive_registered_tool_needs_explicit_approval")
        elif decision == "allow_read_only_tool_plan":
            reasons.append("all_tools_are_registered_active_trusted_read_only_and_route_allowed")

    expected_decision = str(case["expected_decision"])
    expected_tools = list(case["expected_tools"])
    expected_approvals = list(case["expected_approvals"])
    expected_blocks = list(case["expected_blocks"])

    return {
        "case": case["name"],
        "incident_id": case["incident_id"],
        "severity": case["severity"],
        "route_decision": case["route_decision"],
        "route_id": case["route_id"],
        "requested_server_label": requested_server,
        "requested_tools": requested_tools,
        "inspected_tools": inspected_tools,
        "decision": decision,
        "allowed_tools": allowed_tools,
        "approval_required_for": approvals,
        "blocked_tools": blocks,
        "expected_decision": expected_decision,
        "expected_tools": expected_tools,
        "expected_approvals": expected_approvals,
        "expected_blocks": expected_blocks,
        "passed": (
            decision == expected_decision
            and allowed_tools == expected_tools
            and approvals == expected_approvals
            and blocks == expected_blocks
        ),
        "reasons": reasons,
        "next_action": case["expected_next_action"],
    }


def simulate_governed_tool_registry() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    decisions = [_decide(case, plan) for case in plan["registry_cases"]]
    passed = sum(1 for item in decisions if item["passed"])
    total = len(decisions)

    return {
        "mode": "governed_tool_registry_simulation_no_runtime",
        "namespace": plan["namespace"],
        "agent_runtime_started": False,
        "mcp_server_started": False,
        "tool_registry_runtime_started": False,
        "tool_calls_executed": False,
        "provider_call_made": False,
        "decisions": decisions,
        "passed_cases": passed,
        "total_cases": total,
        "score": passed / total if total else 0.0,
        "status": "pass" if passed == total else "fail",
    }


def main() -> int:
    result = simulate_governed_tool_registry()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
