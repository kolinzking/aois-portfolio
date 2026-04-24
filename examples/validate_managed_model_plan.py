#!/usr/bin/env python3
"""Validate Phase 4 v10 managed model plan without cloud calls."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("cloud/aws/bedrock-model-layer.plan.json")


def validate_managed_model_plan() -> dict[str, object]:
    missing: list[str] = []

    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    required_top_level = [
        "mode",
        "provider",
        "region",
        "model_id",
        "provider_call_made",
        "credentials_required_for_this_lesson",
        "external_network_required_for_this_lesson",
        "budget",
        "request_contract",
        "controls",
    ]
    for key in required_top_level:
        if key not in plan:
            missing.append(f"missing_key:{key}")

    if plan.get("provider_call_made") is not False:
        missing.append("provider_call_made_must_be_false")
    if plan.get("credentials_required_for_this_lesson") is not False:
        missing.append("credentials_must_not_be_required")
    if plan.get("external_network_required_for_this_lesson") is not False:
        missing.append("network_must_not_be_required")

    budget = plan.get("budget", {})
    if not isinstance(budget, dict) or budget.get("approved") is not False:
        missing.append("budget_must_not_be_approved")
    if isinstance(budget, dict) and budget.get("max_spend_usd") != 0:
        missing.append("max_spend_must_be_zero")

    controls = plan.get("controls", {})
    for key in [
        "security_inspection_required",
        "provider_gate_required",
        "trace_id_required",
        "eval_baseline_required",
        "resource_usage_record_required",
    ]:
        if not isinstance(controls, dict) or controls.get(key) is not True:
            missing.append(f"control_missing:{key}")

    return {
        "mode": "managed_model_plan_validation_no_cloud_call",
        "cloud_call_made": False,
        "credentials_used": False,
        "plan": str(PLAN_PATH),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_managed_model_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
