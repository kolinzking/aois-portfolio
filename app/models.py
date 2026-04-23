from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class AnalyzeRequest(BaseModel):
    log: str = Field(min_length=5, max_length=1000)


class AnalyzeResponse(BaseModel):
    summary: str
    severity: Severity
    suggestion: str
    source: str = "regex"


class HealthResponse(BaseModel):
    status: str
    app_name: str
    environment: str
