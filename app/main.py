"""FastAPI entrypoint for AOIS.

This module is authored in Phase 0 v0.6.
It imports FastAPI only when the dependency is installed, so earlier
standard-library validation can still explain the intended service shape.
"""

from __future__ import annotations

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover - exercised before dependency install
    raise RuntimeError(
        "FastAPI dependencies are not installed. "
        "Install the v0.6 runtime dependencies before running app.main."
    ) from exc

from app.analysis import analyze_incident
from app.ai_contract import analyze_with_structured_contract
from app.config import load_settings
from app.models import IncidentInput


class AnalyzeRequest(BaseModel):
    """HTTP request body for deterministic AOIS analysis."""

    message: str = Field(min_length=1)
    source: str = Field(default="api", min_length=1)


class AnalyzeResponse(BaseModel):
    """HTTP response body for deterministic AOIS analysis."""

    category: str
    severity: str
    confidence: float
    summary: str
    recommended_action: str


class AIAnalyzeRequest(BaseModel):
    """HTTP request body for provider-gated structured AI analysis."""

    message: str = Field(min_length=1)
    source: str = Field(default="api", min_length=1)
    allow_provider_call: bool = False


class AIAnalyzeResponse(BaseModel):
    """Structured response shape expected from future AI analysis."""

    category: str
    severity: str
    confidence: float
    summary: str
    recommended_action: str
    reasoning: str
    provider_mode: str
    provider_call_made: bool
    prompt_contract: dict[str, object]


settings = load_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Return a minimal health signal."""

    return {"status": "ok", "environment": settings.environment}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze an incident message through the deterministic Python layer."""

    result = analyze_incident(
        IncidentInput(message=request.message, source=request.source)
    )
    return AnalyzeResponse(
        category=result.category,
        severity=result.severity.value,
        confidence=result.confidence,
        summary=result.summary,
        recommended_action=result.recommended_action,
    )


@app.post("/ai/analyze", response_model=AIAnalyzeResponse)
def ai_analyze(request: AIAnalyzeRequest) -> AIAnalyzeResponse:
    """Return the Phase 1 structured AI contract without provider execution."""

    if request.allow_provider_call:
        raise HTTPException(
            status_code=403,
            detail=(
                "External AI provider calls are disabled in v1 unless an explicit "
                "budget, provider, key-storage plan, and approval are recorded."
            ),
        )

    result = analyze_with_structured_contract(
        IncidentInput(message=request.message, source=request.source)
    )
    return AIAnalyzeResponse(
        category=result.category,
        severity=result.severity,
        confidence=result.confidence,
        summary=result.summary,
        recommended_action=result.recommended_action,
        reasoning=result.reasoning,
        provider_mode=result.provider_mode,
        provider_call_made=result.provider_call_made,
        prompt_contract=result.prompt_contract,
    )
