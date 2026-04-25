#!/usr/bin/env python3
"""Simulate Phase 6 v19 chaos game-day decisions without fault injection."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("chaos/aois-p/chaos-engineering.plan.json")


SIMULATED_GAME_DAY = [
    {
        "experiment": "aois-p-api-latency-game-day",
        "steady_state_confirmed": True,
        "slo_budget_available": True,
        "primary_aois_excluded": True,
        "abort_condition_seen": False,
        "decision": "approved_for_tabletop_only",
    },
    {
        "experiment": "aois-p-stream-lag-game-day",
        "steady_state_confirmed": True,
        "slo_budget_available": True,
        "primary_aois_excluded": True,
        "abort_condition_seen": False,
        "decision": "approved_for_tabletop_only",
    },
    {
        "experiment": "aois-p-agent-bad-recommendation-game-day",
        "steady_state_confirmed": True,
        "slo_budget_available": False,
        "primary_aois_excluded": True,
        "abort_condition_seen": True,
        "decision": "blocked",
    },
]


def _evaluate(item: dict[str, object]) -> dict[str, object]:
    blockers: list[str] = []
    if item["steady_state_confirmed"] is not True:
        blockers.append("steady_state_not_confirmed")
    if item["slo_budget_available"] is not True:
        blockers.append("slo_budget_unavailable")
    if item["primary_aois_excluded"] is not True:
        blockers.append("primary_aois_not_excluded")
    if item["abort_condition_seen"] is True:
        blockers.append("abort_condition_seen")

    if blockers:
        decision = "blocked"
        action = "do not run chaos; fix guardrails and review"
    else:
        decision = str(item["decision"])
        action = "run tabletop discussion only; no live fault injection"

    return {
        "experiment": item["experiment"],
        "blockers": blockers,
        "decision": decision,
        "recommended_action": action,
    }


def simulate_chaos_game_day() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    evaluations = [_evaluate(item) for item in SIMULATED_GAME_DAY]
    blocked = [item["experiment"] for item in evaluations if item["decision"] == "blocked"]

    return {
        "mode": "chaos_game_day_simulation_no_fault_injection",
        "namespace": plan["namespace"],
        "chaos_runtime_started": False,
        "fault_injection_executed": False,
        "load_test_started": False,
        "network_fault_started": False,
        "cpu_stress_started": False,
        "memory_stress_started": False,
        "pod_delete_executed": False,
        "agent_runtime_started": False,
        "provider_call_made": False,
        "evaluations": evaluations,
        "blocked_experiments": blocked,
        "status": "pass",
    }


def main() -> int:
    result = simulate_chaos_game_day()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
