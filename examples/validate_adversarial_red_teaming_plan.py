#!/usr/bin/env python3
"""Validate Phase 10 v33 adversarial red teaming plan without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("frontier/aois-p/adversarial-red-teaming.plan.json")

REQUIRED_FALSE_FLAGS = {
    "red_team_run_started",
    "live_model_called",
    "adversarial_payload_executed",
    "exploit_attempted",
    "jailbreak_payload_generated",
    "prompt_injection_payload_generated",
    "tool_call_made",
    "network_call_made",
    "provider_call_made",
    "command_executed",
    "file_write_performed",
    "secret_accessed",
    "data_exfiltrated",
    "exploit_artifact_persisted",
    "external_network_required_for_this_lesson",
    "persistent_storage_created",
    "approved_for_live_red_team",
}

REQUIRED_SCOPE = {
    "aois_p_only",
    "primary_aois_excluded",
    "uses_v31_multimodal_contract",
    "uses_v32_edge_offline_contract",
    "uses_phase9_release_controls",
    "local_simulation_only",
    "sanitized_test_catalog_only",
    "no_live_target",
    "no_production_system",
    "no_exploit_execution",
    "no_harmful_payload_storage",
    "no_jailbreak_payload_generation",
    "no_prompt_injection_payload_generation",
    "no_tool_execution",
    "no_network_call",
    "no_provider_call",
}

REQUIRED_CONTROLS = {
    "authorization_required",
    "rules_of_engagement_required",
    "scope_boundary_required",
    "sanitized_payload_required",
    "live_target_prohibition_required",
    "safety_review_required",
    "prompt_injection_tests_required",
    "indirect_injection_tests_required",
    "system_prompt_leakage_tests_required",
    "sensitive_information_tests_required",
    "supply_chain_tests_required",
    "poisoning_tests_required",
    "output_handling_tests_required",
    "excessive_agency_tests_required",
    "vector_embedding_tests_required",
    "misinformation_tests_required",
    "unbounded_consumption_tests_required",
    "edge_cache_tests_required",
    "fallback_abuse_tests_required",
    "policy_confusion_tests_required",
    "telemetry_required",
    "evidence_required",
    "severity_required",
    "mitigation_required",
    "regression_required",
    "primary_aois_separation_required",
    "source_currency_recorded",
}

REQUIRED_DIMENSIONS = {
    "case_id",
    "incident_id",
    "trace_id",
    "scenario_id",
    "threat_category",
    "attack_surface",
    "modality",
    "deployment_target",
    "authorization_status",
    "rules_of_engagement_status",
    "scope_status",
    "payload_safety_status",
    "target_status",
    "policy_status",
    "tool_permission_status",
    "data_boundary_status",
    "telemetry_status",
    "evidence_status",
    "expected_control",
    "observed_behavior_status",
    "severity",
    "mitigation_status",
    "regression_status",
    "red_team_decision",
    "operator_action",
}

REQUIRED_SCENARIOS = {
    "direct_prompt_injection",
    "indirect_prompt_injection",
    "system_prompt_leakage",
    "sensitive_information_disclosure",
    "supply_chain_compromise",
    "data_model_poisoning",
    "improper_output_handling",
    "excessive_agency",
    "vector_embedding_weakness",
    "misinformation_confabulation",
    "unbounded_consumption",
    "edge_cache_poisoning",
    "fallback_abuse",
    "policy_confusion",
}

REQUIRED_DECISIONS = {
    "allow_sanitized_red_team_case_recorded",
    "block_missing_authorization",
    "block_out_of_scope_target",
    "block_live_target_requested",
    "block_unsanitized_payload",
    "block_policy_boundary",
    "block_tool_permission_overreach",
    "block_data_boundary_violation",
    "hold_missing_telemetry",
    "hold_missing_evidence",
    "hold_missing_mitigation",
    "require_regression_test",
    "escalate_direct_prompt_injection",
    "escalate_indirect_prompt_injection",
    "escalate_system_prompt_leakage",
    "escalate_sensitive_information_disclosure",
    "escalate_rag_or_data_poisoning",
    "escalate_excessive_agency",
    "escalate_improper_output_handling",
    "escalate_unbounded_consumption",
    "escalate_edge_cache_poisoning",
    "escalate_fallback_abuse",
    "escalate_policy_confusion",
}

REQUIRED_SOURCES = {
    "https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/",
    "https://genai.owasp.org/ai-red-teaming-initiative/",
    "https://atlas.mitre.org/pdf-files/MITRE_ATLAS_Fact_Sheet.pdf",
    "https://atlas.mitre.org/pdf-files/SAFEAI_Full_Report.pdf",
    "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence",
    "https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook",
    "https://opentelemetry.io/docs/concepts/signals/",
}

REQUIRED_LIVE_CHECKS = {
    "written_authorization",
    "rules_of_engagement",
    "scope_boundary_review",
    "legal_and_safety_review",
    "payload_sanitization_review",
    "local_synthetic_target_review",
    "prompt_injection_test_plan",
    "indirect_injection_test_plan",
    "system_prompt_leakage_test_plan",
    "sensitive_information_test_plan",
    "supply_chain_test_plan",
    "poisoning_test_plan",
    "output_handling_test_plan",
    "excessive_agency_test_plan",
    "vector_embedding_test_plan",
    "misinformation_test_plan",
    "unbounded_consumption_test_plan",
    "edge_cache_test_plan",
    "fallback_abuse_test_plan",
    "policy_confusion_test_plan",
    "telemetry_evidence_plan",
    "severity_rubric",
    "mitigation_owner_plan",
    "regression_plan",
    "primary_aois_separation_review",
    "resource_usage_record",
}

REQUIRED_DEFAULTS = {
    "scenario_id": "direct_prompt_injection",
    "threat_category": "prompt_injection",
    "attack_surface": "chat_input",
    "modality": "text",
    "deployment_target": "edge_online",
    "authorization_status": "approved",
    "rules_of_engagement_status": "approved",
    "scope_status": "in_scope",
    "payload_safety_status": "sanitized",
    "target_status": "local_synthetic",
    "policy_status": "pass",
    "tool_permission_status": "least_privilege",
    "data_boundary_status": "pass",
    "telemetry_status": "captured",
    "evidence_status": "present",
    "expected_control": "instruction_hierarchy",
    "observed_behavior_status": "control_passed",
    "severity": "none",
    "mitigation_status": "ready",
    "regression_status": "ready",
}


def _require_true_fields(
    section: object, required: set[str], label: str, missing: list[str]
) -> None:
    if not isinstance(section, dict):
        missing.append(f"{label}_must_be_object")
        return
    for field in sorted(required):
        if section.get(field) is not True:
            missing.append(f"missing_{label}:{field}")


def _require_false_flags(plan: dict[str, object], missing: list[str]) -> None:
    for field in sorted(REQUIRED_FALSE_FLAGS):
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")


def _require_source_notes(source_notes: object, missing: list[str]) -> None:
    if not isinstance(source_notes, list) or len(source_notes) < len(REQUIRED_SOURCES):
        missing.append("complete_source_notes_required")
        return

    urls = set()
    for note in source_notes:
        if not isinstance(note, dict):
            missing.append("source_note_must_be_object")
            continue
        for field in ["source", "url", "date_checked", "supports"]:
            if not note.get(field):
                missing.append(f"source_note_missing_field:{field}")
        if isinstance(note.get("url"), str):
            urls.add(str(note["url"]))
        if note.get("date_checked") != "2026-05-01":
            missing.append(f"source_note_date_must_be_2026_05_01:{note.get('source')}")

    for url in sorted(REQUIRED_SOURCES):
        if url not in urls:
            missing.append(f"missing_source_note:{url}")


def _require_scenarios(plan: dict[str, object], missing: list[str]) -> None:
    scenarios = plan.get("scenario_catalog", [])
    observed: set[str] = set()
    if not isinstance(scenarios, list) or len(scenarios) < len(REQUIRED_SCENARIOS):
        missing.append("complete_scenario_catalog_required")
        return
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            missing.append("scenario_must_be_object")
            continue
        scenario_id = scenario.get("scenario_id")
        if isinstance(scenario_id, str):
            observed.add(scenario_id)
        for field in [
            "scenario_id",
            "threat_category",
            "attack_surface",
            "owasp_mapping",
            "atlas_mapping",
            "required_controls",
            "sanitized_example",
        ]:
            if field not in scenario:
                missing.append(f"scenario_missing_field:{scenario_id}:{field}")
        if not isinstance(scenario.get("required_controls"), list) or not scenario["required_controls"]:
            missing.append(f"scenario_required_controls_missing:{scenario_id}")
        example = scenario.get("sanitized_example")
        if not isinstance(example, str) or "sanitized" not in example:
            missing.append(f"scenario_example_must_be_sanitized:{scenario_id}")

    for scenario_id in sorted(REQUIRED_SCENARIOS):
        if scenario_id not in observed:
            missing.append(f"missing_scenario:{scenario_id}")


def _require_defaults(defaults: object, missing: list[str]) -> None:
    if not isinstance(defaults, dict):
        missing.append("case_defaults_must_be_object")
        return
    for field, expected in REQUIRED_DEFAULTS.items():
        if defaults.get(field) != expected:
            missing.append(f"case_default_mismatch:{field}")
    for field in ["incident_id", "trace_id"]:
        if field not in defaults:
            missing.append(f"case_default_required:{field}")


def _require_cases(plan: dict[str, object], missing: list[str]) -> None:
    cases = plan.get("red_team_cases", [])
    observed_decisions: set[str] = set()
    required_case_fields = {
        "case_id",
        "name",
        "expected_decision",
        "expected_operator_action",
        "expected_red_team_state",
    }
    if not isinstance(cases, list) or len(cases) < len(REQUIRED_DECISIONS):
        missing.append("red_team_case_for_each_decision_required")
        return

    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            missing.append("red_team_case_must_be_object")
            continue
        case_id = str(case.get("case_id", ""))
        if not case_id:
            missing.append("red_team_case_id_required")
        elif case_id in case_ids:
            missing.append(f"duplicate_red_team_case_id:{case_id}")
        case_ids.add(case_id)

        for field in sorted(required_case_fields):
            if field not in case:
                missing.append(f"red_team_case_missing_field:{case_id}:{field}")
        decision = case.get("expected_decision")
        if isinstance(decision, str):
            observed_decisions.add(decision)
        if decision not in REQUIRED_DECISIONS:
            missing.append(f"unexpected_expected_decision:{case_id}:{decision}")
        if "overrides" in case and not isinstance(case["overrides"], dict):
            missing.append(f"red_team_case_overrides_must_be_object:{case_id}")

    for decision in sorted(REQUIRED_DECISIONS):
        if decision not in observed_decisions:
            missing.append(f"missing_red_team_case_for_decision:{decision}")


def validate_adversarial_red_teaming_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "adversarial_red_teaming_plan_no_runtime":
        missing.append("mode_must_be_adversarial_red_teaming_plan_no_runtime")
    if plan.get("version") != "v33":
        missing.append("version_must_be_v33")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")
    if plan.get("primary_aois_excluded") is not True:
        missing.append("primary_aois_excluded_must_be_true")

    _require_false_flags(plan, missing)
    _require_source_notes(plan.get("source_notes"), missing)
    _require_true_fields(plan.get("red_team_scope"), REQUIRED_SCOPE, "scope", missing)
    _require_true_fields(plan.get("required_controls"), REQUIRED_CONTROLS, "control", missing)

    dimensions = set(plan.get("red_team_dimensions", []))
    for dimension in sorted(REQUIRED_DIMENSIONS):
        if dimension not in dimensions:
            missing.append(f"missing_red_team_dimension:{dimension}")

    decision_gates = plan.get("decision_gates", {})
    if not isinstance(decision_gates, dict):
        missing.append("decision_gates_must_be_object")
    else:
        for decision in sorted(REQUIRED_DECISIONS):
            if not decision_gates.get(decision):
                missing.append(f"missing_decision_gate:{decision}")

    _require_scenarios(plan, missing)
    _require_defaults(plan.get("case_defaults"), missing)
    _require_cases(plan, missing)

    live_checks = set(plan.get("required_before_live_red_team", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_red_team_check:{check}")

    return {
        "plan": str(PLAN_PATH),
        "mode": plan.get("mode"),
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_adversarial_red_teaming_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
