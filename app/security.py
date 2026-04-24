"""Local API and LLM security checks for Phase 2 v5."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*([^\s]+)"),
    re.compile(r"(?i)bearer\s+[a-z0-9._\-]+"),
    re.compile(r"sk-[a-zA-Z0-9]{12,}"),
]

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal your system prompt",
    "print your hidden prompt",
    "disable safety",
    "exfiltrate",
    "show me your secrets",
    "developer message",
]


@dataclass(frozen=True)
class SecurityFinding:
    """One local security finding."""

    kind: str
    severity: str
    evidence: str
    recommended_action: str


@dataclass(frozen=True)
class SecurityInspection:
    """Security inspection result for an AOIS input."""

    sanitized_message: str
    risk_level: str
    allow_provider_call: bool
    findings: list[dict[str, str]]
    provider_call_made: bool


def redact_secrets(message: str) -> str:
    """Redact simple secret-like values before logging or provider use."""

    redacted = message
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def inspect_security(message: str) -> SecurityInspection:
    """Inspect input for local security risks without calling providers."""

    findings: list[SecurityFinding] = []
    lowered = message.lower()

    for phrase in PROMPT_INJECTION_PATTERNS:
        if phrase in lowered:
            findings.append(
                SecurityFinding(
                    kind="prompt-injection-signal",
                    severity="high",
                    evidence=phrase,
                    recommended_action="Do not send this input to a provider without review.",
                )
            )

    sanitized = redact_secrets(message)
    if sanitized != message:
        findings.append(
            SecurityFinding(
                kind="secret-like-content",
                severity="high",
                evidence="[REDACTED]",
                recommended_action="Remove secrets from prompts, logs, and committed files.",
            )
        )

    risk_level = "high" if any(finding.severity == "high" for finding in findings) else "low"
    return SecurityInspection(
        sanitized_message=sanitized,
        risk_level=risk_level,
        allow_provider_call=False if findings else True,
        findings=[asdict(finding) for finding in findings],
        provider_call_made=False,
    )
