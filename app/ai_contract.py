"""Structured AI contract helpers for Phase 1 without provider calls."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from app.analysis import analyze_incident
from app.models import IncidentInput


STRUCTURED_AI_FIELDS = [
    "category",
    "severity",
    "confidence",
    "summary",
    "recommended_action",
    "reasoning",
]


@dataclass(frozen=True)
class StructuredPromptContract:
    """Prompt contract that a future provider call must satisfy."""

    system_prompt: str
    user_prompt: str
    required_fields: list[str]
    response_format: str = "json_object"


@dataclass(frozen=True)
class StructuredAIAnalysis:
    """Provider-neutral structured AI response shape."""

    category: str
    severity: str
    confidence: float
    summary: str
    recommended_action: str
    reasoning: str
    provider_mode: str
    provider_call_made: bool
    prompt_contract: dict[str, object]


def build_prompt_contract(incident: IncidentInput) -> StructuredPromptContract:
    return StructuredPromptContract(
        system_prompt=(
            "You are AOIS, an operations intelligence assistant. "
            "Return only structured incident analysis fields."
        ),
        user_prompt=f"Analyze this incident signal: {incident.message}",
        required_fields=STRUCTURED_AI_FIELDS,
    )


def analyze_with_structured_contract(incident: IncidentInput) -> StructuredAIAnalysis:
    """Return a structured response contract without calling an AI provider."""

    deterministic = analyze_incident(incident)
    prompt_contract = build_prompt_contract(incident)
    return StructuredAIAnalysis(
        category=deterministic.category,
        severity=deterministic.severity.value,
        confidence=deterministic.confidence,
        summary=deterministic.summary,
        recommended_action=deterministic.recommended_action,
        reasoning=(
            "Dry-run structured contract: deterministic baseline result is wrapped "
            "in the same fields a future AI provider must return."
        ),
        provider_mode="dry_run_structured_contract",
        provider_call_made=False,
        prompt_contract=asdict(prompt_contract),
    )
