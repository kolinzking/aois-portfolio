#!/usr/bin/env python3
"""Validate Phase 6 v17 event streaming plan without broker runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("streaming/aois-p/event-streaming.plan.json")

REQUIRED_FIELDS = {
    "event_id",
    "event_type",
    "schema_version",
    "trace_id",
    "incident_id",
    "producer",
    "created_at",
    "payload",
}

REQUIRED_EVENT_TYPES = {
    "incident.received",
    "incident.classified",
    "incident.routed",
    "incident.recommended",
}

REQUIRED_DURABILITY = {
    "retention_policy_required",
    "dead_letter_stream_required",
    "replay_policy_required",
    "schema_compatibility_required",
    "backpressure_policy_required",
    "poison_event_policy_required",
}

REQUIRED_LIVE_CHECKS = {
    "broker_selection_review",
    "schema_registry_plan",
    "retention_policy",
    "producer_retry_policy",
    "consumer_offset_policy",
    "dead_letter_stream_plan",
    "replay_runbook",
    "lag_dashboard",
    "storage_budget",
    "rollback_plan",
    "primary_aois_separation_review",
}


def validate_event_streaming_plan() -> dict[str, object]:
    missing: list[str] = []
    if not PLAN_PATH.exists():
        missing.append(f"missing_file:{PLAN_PATH}")
        plan: dict[str, object] = {}
    else:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    if plan.get("mode") != "event_streaming_plan_no_broker":
        missing.append("mode_must_be_no_broker")
    if plan.get("namespace") != "aois-p":
        missing.append("namespace_must_be_aois_p")

    for field in [
        "stream_runtime_started",
        "broker_started",
        "kafka_started",
        "redis_stream_started",
        "nats_started",
        "producer_started",
        "consumer_started",
        "external_network_required_for_this_lesson",
        "approved_for_live_streaming",
    ]:
        if plan.get(field) is not False:
            missing.append(f"{field}_must_be_false")

    stream = plan.get("stream", {})
    if not isinstance(stream, dict):
        missing.append("stream_must_be_object")
    else:
        for field in ["name"]:
            value = stream.get(field)
            if not isinstance(value, str) or not value.startswith("aois-p-"):
                missing.append(f"stream_field_must_use_aois_p_prefix:{field}")
        if stream.get("topic") != "aois-p.incident.events":
            missing.append("topic_must_be_aois_p_incident_events")
        for field in ["event_id_required", "schema_version_required", "ordering_key_required"]:
            if stream.get(field) is not True:
                missing.append(f"missing_stream_control:{field}")

    contract = plan.get("event_contract", {})
    if not isinstance(contract, dict):
        missing.append("event_contract_must_be_object")
    else:
        fields = set(contract.get("required_fields", []))
        for field in sorted(REQUIRED_FIELDS):
            if field not in fields:
                missing.append(f"missing_event_field:{field}")
        event_types = set(contract.get("event_types", []))
        for event_type in sorted(REQUIRED_EVENT_TYPES):
            if event_type not in event_types:
                missing.append(f"missing_event_type:{event_type}")
        if contract.get("payload_policy") != "small_event_with_pointer_for_large_payload":
            missing.append("payload_policy_must_use_pointer_for_large_payload")

    producer = plan.get("producer_plan", {})
    if not isinstance(producer, dict):
        missing.append("producer_plan_must_be_object")
    else:
        if not str(producer.get("name", "")).startswith("aois-p-"):
            missing.append("producer_name_must_use_aois_p_prefix")
        for field in [
            "idempotency_key_required",
            "delivery_ack_required",
            "retry_policy_required",
            "schema_validation_required",
        ]:
            if producer.get(field) is not True:
                missing.append(f"missing_producer_control:{field}")

    consumer = plan.get("consumer_plan", {})
    if not isinstance(consumer, dict):
        missing.append("consumer_plan_must_be_object")
    else:
        for field in ["name", "consumer_group"]:
            if not str(consumer.get(field, "")).startswith("aois-p-"):
                missing.append(f"consumer_field_must_use_aois_p_prefix:{field}")
        for field in [
            "offset_tracking_required",
            "lag_measurement_required",
            "idempotent_processing_required",
            "dead_letter_stream_required",
            "replay_runbook_required",
        ]:
            if consumer.get(field) is not True:
                missing.append(f"missing_consumer_control:{field}")

    durability = plan.get("durability_controls", {})
    if not isinstance(durability, dict):
        missing.append("durability_controls_must_be_object")
    else:
        for field in sorted(REQUIRED_DURABILITY):
            if durability.get(field) is not True:
                missing.append(f"missing_durability_control:{field}")

    limits = plan.get("limits", {})
    if not isinstance(limits, dict):
        missing.append("limits_must_be_object")
    else:
        for field in [
            "max_brokers_for_lesson",
            "max_producers_for_lesson",
            "max_consumers_for_lesson",
            "max_persistent_storage_mb",
            "max_network_calls",
        ]:
            if limits.get(field) != 0:
                missing.append(f"{field}_must_be_zero")

    live_checks = set(plan.get("required_before_live_streaming", []))
    for check in sorted(REQUIRED_LIVE_CHECKS):
        if check not in live_checks:
            missing.append(f"missing_live_check:{check}")

    return {
        "mode": "event_streaming_validation_no_broker",
        "stream_runtime_started": False,
        "broker_started": False,
        "producer_started": False,
        "consumer_started": False,
        "namespace": plan.get("namespace"),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_event_streaming_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
