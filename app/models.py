"""Core AOIS data models for the Phase 0 Python foundation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    """Small severity vocabulary used before AI scoring is introduced."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class IncidentInput:
    """Raw incident signal accepted by the Python analysis layer."""

    message: str
    source: str = "manual"

    def __post_init__(self) -> None:
        if not self.message.strip():
            raise ValueError("incident message must not be empty")
        if not self.source.strip():
            raise ValueError("incident source must not be empty")


@dataclass(frozen=True)
class AnalysisResult:
    """Deterministic first-pass incident interpretation."""

    category: str
    severity: Severity
    summary: str
    recommended_action: str
    confidence: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
