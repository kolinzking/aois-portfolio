#!/usr/bin/env python3
"""Validate Phase 5 v15 fine-tuning plan without training."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/fine-tuning-adaptation.plan.json")

REQUIRED_OPTIONS = {
    "no_tuning_baseline",
    "prompt_or_routing_adjustment",
    "lora_style_placeholder",
    "full_fine_tune_placeholder",
}

REQUIRED_DATASET_CONTROLS = {
    "dataset_card_required",
    "pii_review_required",
    "license_review_required",
    "train_validation_split_required",
    "holdout_eval_required",
    "data_version_required",
    "leakage_check_required",
}

REQUIRED_EVAL_CONTROLS = {
    "baseline_eval_required",
    "adapted_eval_required",
    "regression_eval_required",
    "overfit_check_required",
    "quality_gate_required",
    "rollback_plan_required",
}

REQUIRED_LIVE_CHECKS = {
    "dataset_card",
    "pii_review",
    "license_review",
    "data_versioning_plan",
    "train_validation_holdout_split",
    "baseline_eval",
    "quality_gate",
    "cost_budget",
    "gpu_or_provider_training_approval",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_fine_tuning_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "fine_tuning_adaptation_plan_no_training":
        missing.append("mode_must_be_no_training")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    for field in [
        "training_job_started",
        "dataset_uploaded",
        "model_downloaded",
        "gpu_runtime_started",
        "external_network_required_for_this_lesson",
        "approved_for_live_training",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    options = plan.get("adaptation_options", [])
    if not isinstance(options, list) or len(options) < 4:
        missing.append("adaptation_options_must_include_four_paths")
    else:
        names = {option.get("name") for option in options if isinstance(option, dict)}
        for name in sorted(REQUIRED_OPTIONS):
            if name not in names:
                missing.append(f"missing_adaptation_option:{name}")

    dataset_controls = plan.get("dataset_controls", {})
    if not isinstance(dataset_controls, dict):
        missing.append("dataset_controls_must_be_object")
    else:
        for field in sorted(REQUIRED_DATASET_CONTROLS):
            if dataset_controls.get(field) is not True:
                missing.append(f"missing_dataset_control:{field}")

    eval_controls = plan.get("eval_controls", {})
    if not isinstance(eval_controls, dict):
        missing.append("eval_controls_must_be_object")
    else:
        for field in sorted(REQUIRED_EVAL_CONTROLS):
            if eval_controls.get(field) is not True:
                missing.append(f"missing_eval_control:{field}")

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in ["max_training_jobs_for_lesson", "max_uploaded_dataset_mb", "max_spend_usd"]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    live_checks = set(plan.get("required_before_live_training", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "fine_tuning_plan_validation_no_training",
        "training_job_started": False,
        "dataset_uploaded": False,
        "model_downloaded": False,
        "gpu_runtime_started": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_fine_tuning_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
