"""FastAPI entrypoint for AOIS.

This module is authored in Phase 0 v0.6.
It imports FastAPI only when the dependency is installed, so earlier
standard-library validation can still explain the intended service shape.
"""

from __future__ import annotations

try:
    from fastapi import FastAPI
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover - exercised before dependency install
    raise RuntimeError(
        "FastAPI dependencies are not installed. "
        "Install the v0.6 runtime dependencies before running app.main."
    ) from exc

from app.analysis import analyze_incident
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


settings = load_settings()
app = FastAPI(title=settings.app_name, version="0.6.0")


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
