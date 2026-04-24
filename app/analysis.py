"""Deterministic incident analysis used before LLM integration."""

from __future__ import annotations

from app.models import AnalysisResult, IncidentInput, Severity


def normalize_message(message: str) -> str:
    """Normalize input enough for deterministic rule matching."""

    return " ".join(message.lower().strip().split())


def analyze_incident(incident: IncidentInput) -> AnalysisResult:
    """Classify a raw incident with explicit, intentionally limited rules."""

    normalized = normalize_message(incident.message)

    if "oomkilled" in normalized or "exit code 137" in normalized:
        return AnalysisResult(
            category="memory-pressure",
            severity=Severity.HIGH,
            summary="The message points to memory pressure or an out-of-memory kill.",
            recommended_action="Inspect memory usage, container limits, and recent restarts.",
            confidence=0.85,
        )

    if "crashloopbackoff" in normalized or "restarting" in normalized:
        return AnalysisResult(
            category="restart-loop",
            severity=Severity.HIGH,
            summary="The message points to a process or workload restart loop.",
            recommended_action="Inspect last exit reason, logs, and recent configuration changes.",
            confidence=0.8,
        )

    if "5xx" in normalized or "gateway" in normalized:
        return AnalysisResult(
            category="service-error",
            severity=Severity.MEDIUM,
            summary="The message points to an HTTP service or upstream error.",
            recommended_action="Inspect the HTTP path, upstream service, and recent deploy.",
            confidence=0.7,
        )

    if "permission denied" in normalized:
        return AnalysisResult(
            category="permission-error",
            severity=Severity.MEDIUM,
            summary="The message points to a permission or execution-context problem.",
            recommended_action="Inspect path, owner, mode, user, and execution context.",
            confidence=0.75,
        )

    return AnalysisResult(
        category="unknown",
        severity=Severity.UNKNOWN,
        summary="No deterministic rule matched this message.",
        recommended_action="Preserve the raw signal and escalate to richer analysis.",
        confidence=0.2,
    )
