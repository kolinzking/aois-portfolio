"""Local reliability helpers for Phase 1 v3."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from uuid import uuid4

from app.analysis import analyze_incident
from app.models import IncidentInput


def new_trace_id() -> str:
    """Create a short local trace id for correlating practice outputs."""

    return f"aois-p-{uuid4().hex[:12]}"


@dataclass(frozen=True)
class EvalCase:
    """A local evaluation case for deterministic AOIS behavior."""

    name: str
    message: str
    expected_category: str
    expected_severity: str


@dataclass(frozen=True)
class EvalCaseResult:
    """Result for one local evaluation case."""

    name: str
    message: str
    expected_category: str
    actual_category: str
    expected_severity: str
    actual_severity: str
    passed: bool


EVAL_CASES = [
    EvalCase(
        name="http_gateway_error",
        message="gateway returned 5xx after deploy",
        expected_category="service-error",
        expected_severity="medium",
    ),
    EvalCase(
        name="memory_pressure",
        message="pod OOMKilled exit code 137",
        expected_category="memory-pressure",
        expected_severity="high",
    ),
    EvalCase(
        name="restart_loop",
        message="pod CrashLoopBackOff restarting",
        expected_category="restart-loop",
        expected_severity="high",
    ),
    EvalCase(
        name="permission_error",
        message="permission denied opening config file",
        expected_category="permission-error",
        expected_severity="medium",
    ),
]


def run_eval_baseline() -> dict[str, object]:
    """Run the local deterministic evaluation baseline."""

    results: list[EvalCaseResult] = []
    for case in EVAL_CASES:
        actual = analyze_incident(IncidentInput(message=case.message, source="eval"))
        passed = (
            actual.category == case.expected_category
            and actual.severity.value == case.expected_severity
        )
        results.append(
            EvalCaseResult(
                name=case.name,
                message=case.message,
                expected_category=case.expected_category,
                actual_category=actual.category,
                expected_severity=case.expected_severity,
                actual_severity=actual.severity.value,
                passed=passed,
            )
        )

    passed_cases = sum(1 for result in results if result.passed)
    total_cases = len(results)
    return {
        "trace_id": new_trace_id(),
        "mode": "local_eval_baseline",
        "provider_call_made": False,
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "score": passed_cases / total_cases if total_cases else 0.0,
        "results": [asdict(result) for result in results],
    }
