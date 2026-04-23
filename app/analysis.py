from __future__ import annotations

import re

from app.models import AnalyzeResponse, Severity


def analyze_log(log: str) -> AnalyzeResponse:
    text = log.strip()

    if re.search(r"oomkilled|exit code 137|memory", text, re.IGNORECASE):
        return AnalyzeResponse(
            summary="The workload likely hit memory pressure and was terminated.",
            severity=Severity.P2,
            suggestion="Increase memory limits and inspect for leaks.",
        )
    if re.search(r"crashloopbackoff|restart", text, re.IGNORECASE):
        return AnalyzeResponse(
            summary="The service is repeatedly restarting and failing to stabilize.",
            severity=Severity.P2,
            suggestion="Inspect the container logs and failing startup dependency.",
        )
    if re.search(r"5xx|502|503|504|gateway", text, re.IGNORECASE):
        return AnalyzeResponse(
            summary="The service is serving upstream or server-side errors.",
            severity=Severity.P3,
            suggestion="Check the upstream dependency and recent deploy changes.",
        )
    if re.search(r"disk|no space left|filesystem", text, re.IGNORECASE):
        return AnalyzeResponse(
            summary="The system is likely hitting storage pressure.",
            severity=Severity.P2,
            suggestion="Free disk space and inspect log or artifact growth.",
        )

    return AnalyzeResponse(
        summary="The issue is not recognized by the current regex classifier.",
        severity=Severity.P4,
        suggestion="Escalate to a richer analyzer because the rule set is too narrow.",
    )
