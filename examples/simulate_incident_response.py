#!/usr/bin/env python3
"""Simulate a Phase 6 v18 incident response timeline without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("incident-response/aois-p/incident-response.plan.json")


def simulate_incident_response() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    roles = plan["roles"]

    timeline = [
        {
            "minute": 0,
            "step": "detect",
            "actor": roles["operations_lead"],
            "evidence": "aois-p-incident-agent valid_recommendation_ratio budget exhausted",
        },
        {
            "minute": 4,
            "step": "triage",
            "actor": roles["incident_commander"],
            "evidence": "impact limited to incident recommendations, API remains available",
        },
        {
            "minute": 8,
            "step": "declare",
            "actor": roles["incident_commander"],
            "severity": "SEV2",
            "reason": "unsafe or low-quality recommendations can slow mitigation",
        },
        {
            "minute": 12,
            "step": "stabilize",
            "actor": roles["agent_operator"],
            "action": "route destructive or low-confidence recommendations to human review",
        },
        {
            "minute": 18,
            "step": "mitigate",
            "actor": roles["operations_lead"],
            "action": "freeze prompt and tool changes while evidence is reviewed",
        },
        {
            "minute": 27,
            "step": "resolve",
            "actor": roles["incident_commander"],
            "criteria": "recommendation quality gate restored in local evaluation set",
        },
        {
            "minute": 45,
            "step": "review",
            "actor": roles["scribe"],
            "action": "create post-incident review with owners and due dates",
        },
    ]

    communications = [
        {
            "minute": 10,
            "audience": "internal",
            "message": "SEV2 declared for incident-agent recommendation quality; API availability unaffected.",
        },
        {
            "minute": 30,
            "audience": "internal",
            "message": "Risky agent actions routed to human review; prompt and tool changes frozen.",
        },
    ]

    action_items = [
        {
            "owner": roles["agent_operator"],
            "item": "expand quality evaluation set for memory-pressure incidents",
            "due_days": 7,
        },
        {
            "owner": roles["operations_lead"],
            "item": "add runbook check for agent SLO exhaustion",
            "due_days": 5,
        },
        {
            "owner": roles["communications_lead"],
            "item": "template internal updates for agent-quality incidents",
            "due_days": 10,
        },
    ]

    return {
        "mode": "incident_response_simulation_no_runtime",
        "namespace": plan["namespace"],
        "incident_runtime_started": False,
        "pager_runtime_started": False,
        "ticketing_runtime_started": False,
        "chatops_runtime_started": False,
        "status_page_runtime_started": False,
        "agent_runtime_started": False,
        "provider_call_made": False,
        "incident": {
            "id": "incident-v18-local-sim",
            "severity": "SEV2",
            "trigger": "agent error budget exhausted",
            "customer_impact": "recommendations require human review before action",
            "resolved": True,
        },
        "timeline": timeline,
        "communications": communications,
        "action_items": action_items,
        "post_incident_review_required": True,
        "status": "pass",
    }


def main() -> int:
    result = simulate_incident_response()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
