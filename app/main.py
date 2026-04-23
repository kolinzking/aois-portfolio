from __future__ import annotations

from fastapi import FastAPI

from app.analysis import analyze_log
from app.config import get_settings
from app.models import AnalyzeRequest, AnalyzeResponse, HealthResponse


settings = get_settings()
app = FastAPI(title=settings["app_name"])


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        app_name=settings["app_name"],
        environment=settings["environment"],
    )


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    return analyze_log(request.log)
