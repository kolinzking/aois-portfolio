#!/usr/bin/env python3
"""Simulate SLO error-budget math for Phase 6 v17.5 without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("reliability/aois-p/service-agent-slo.plan.json")


SAMPLE_WINDOWS = {
    "aois-p-api": {
        "total_events": 10_000,
        "bad_events": 75,
        "burned_in_current_window": 75,
    },
    "aois-p-incident-stream-consumer": {
        "total_events": 1_000,
        "bad_events": 8,
        "burned_in_current_window": 8,
    },
    "aois-p-incident-agent": {
        "total_events": 200,
        "bad_events": 14,
        "burned_in_current_window": 14,
    },
}


def _evaluate_slo(entry: dict[str, object]) -> dict[str, object]:
    name = str(entry["name"])
    sample = SAMPLE_WINDOWS[name]
    total_events = int(sample["total_events"])
    bad_events = int(sample["bad_events"])
    objective_percent = float(entry["objective_percent"])
    allowed_bad_events = total_events * ((100.0 - objective_percent) / 100.0)
    good_events = total_events - bad_events
    achieved_percent = (good_events / total_events) * 100.0
    remaining_budget_events = allowed_bad_events - bad_events
    budget_remaining_percent = (remaining_budget_events / allowed_bad_events) * 100.0

    if remaining_budget_events < 0:
        action = "freeze risky changes and route affected work to human review"
    elif budget_remaining_percent < 25:
        action = "slow change rate and investigate burn"
    else:
        action = "continue normal change policy"

    return {
        "name": name,
        "sli": entry["sli"],
        "objective_percent": objective_percent,
        "achieved_percent": round(achieved_percent, 2),
        "total_events": total_events,
        "bad_events": bad_events,
        "allowed_bad_events": round(allowed_bad_events, 2),
        "remaining_budget_events": round(remaining_budget_events, 2),
        "budget_remaining_percent": round(budget_remaining_percent, 2),
        "budget_exhausted": remaining_budget_events < 0,
        "recommended_action": action,
    }


def simulate_slo_error_budget() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    slo_entries = list(plan["service_slos"]) + list(plan["agent_slos"])
    evaluations = [_evaluate_slo(entry) for entry in slo_entries]
    exhausted = [item["name"] for item in evaluations if item["budget_exhausted"]]

    return {
        "mode": "slo_error_budget_simulation_no_runtime",
        "namespace": plan["namespace"],
        "slo_runtime_started": False,
        "metrics_backend_started": False,
        "alerting_runtime_started": False,
        "dashboard_runtime_started": False,
        "agent_runtime_started": False,
        "provider_call_made": False,
        "evaluations": evaluations,
        "budgets_exhausted": exhausted,
        "status": "pass",
    }


def main() -> int:
    result = simulate_slo_error_budget()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
