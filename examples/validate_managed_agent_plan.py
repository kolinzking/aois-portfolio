#!/usr/bin/env python3
"""Validate Phase 4 v10.5 managed-agent tradeoff plan without cloud calls."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("cloud/aws/managed-agent-tradeoff.plan.json")


def validate_managed_agent_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("cloud_agent_created") is not False:
        missing.append("cloud_agent_created_must_be_false")
    if plan.get("credentials_used") is not False:
        missing.append("credentials_used_must_be_false")
    if plan.get("external_network_required_for_this_lesson") is not False:
        missing.append("network_must_not_be_required")

    options = plan.get("options", [])
    if not isinstance(options, list) or len(options) < 2:
        missing.append("options_need_owned_and_managed_paths")
    else:
        names = {option.get("name") for option in options if isinstance(option, dict)}
        if "aois-owned-agent-runtime" not in names:
            missing.append("missing_owned_agent_option")
        if "managed-cloud-agent-placeholder" not in names:
            missing.append("missing_managed_agent_option")

    decision = plan.get("decision", {})
    if not isinstance(decision, dict) or decision.get("current_choice") != "aois-owned-agent-runtime":
        missing.append("current_choice_must_remain_aois_owned")

    required = set(plan.get("required_before_managed_agent", []))
    for item in [
        "official_provider_docs_review",
        "credential_storage_plan",
        "budget_approval",
        "data_boundary_review",
        "tool_permission_review",
        "eval_baseline",
        "rollback_plan",
    ]:
        if item not in required:
            missing.append(f"missing_requirement:{item}")

    return {
        "mode": "managed_agent_plan_validation_no_cloud_call",
        "cloud_agent_created": False,
        "credentials_used": False,
        "plan": str(PLAN_PATH),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_managed_agent_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
