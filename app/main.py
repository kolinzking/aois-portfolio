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
from app.model_router import RouteConstraints, choose_model_route


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


class AIRouteRequest(BaseModel):
    """HTTP request body for model route planning."""

    message: str = Field(min_length=1)
    source: str = Field(default="api", min_length=1)
    severity_hint: str | None = Field(default=None, pattern="^(low|medium|high|unknown)$")
    latency_budget_ms: int = Field(default=1000, ge=1)
    max_cost_usd: float = Field(default=0.001, ge=0)
    provider_budget_approved: bool = False


class AIRouteResponse(BaseModel):
    """Provider-neutral route decision response."""

    severity_used: str
    selected_route: dict[str, object]
    fallback_route: dict[str, object]
    reason: str
    provider_call_made: bool


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


@app.post("/ai/route", response_model=AIRouteResponse)
def ai_route(request: AIRouteRequest) -> AIRouteResponse:
    """Plan model routing without provider execution."""

    baseline = analyze_incident(
        IncidentInput(message=request.message, source=request.source)
    )
    severity = request.severity_hint or baseline.severity.value
    decision = choose_model_route(
        RouteConstraints(
            severity=severity,
            latency_budget_ms=request.latency_budget_ms,
            max_cost_usd=request.max_cost_usd,
            provider_budget_approved=request.provider_budget_approved,
        )
    )
    return AIRouteResponse(
        severity_used=severity,
        selected_route=decision.selected_route,
        fallback_route=decision.fallback_route,
        reason=decision.reason,
        provider_call_made=decision.provider_call_made,
    )
