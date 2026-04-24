"""Provider-neutral model routing decisions for Phase 1 v2."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RouteConstraints:
    """Operational constraints used before model execution."""

    severity: str
    latency_budget_ms: int
    max_cost_usd: float
    provider_budget_approved: bool


@dataclass(frozen=True)
class RouteOption:
    """A route AOIS could use after provider integration is approved."""

    route_name: str
    model: str
    provider: str
    estimated_latency_ms: int
    estimated_cost_usd: float
    requires_external_provider: bool


@dataclass(frozen=True)
class RouteDecision:
    """Selected route and fallback plan without making a provider call."""

    selected_route: dict[str, object]
    fallback_route: dict[str, object]
    reason: str
    provider_call_made: bool


LOCAL_BASELINE = RouteOption(
    route_name="local-baseline",
    model="deterministic-rules",
    provider="local",
    estimated_latency_ms=25,
    estimated_cost_usd=0.0,
    requires_external_provider=False,
)

FAST_EXTERNAL = RouteOption(
    route_name="fast-external-placeholder",
    model="fast-model-placeholder",
    provider="provider-gated",
    estimated_latency_ms=450,
    estimated_cost_usd=0.0003,
    requires_external_provider=True,
)

STRONG_EXTERNAL = RouteOption(
    route_name="strong-external-placeholder",
    model="strong-model-placeholder",
    provider="provider-gated",
    estimated_latency_ms=1500,
    estimated_cost_usd=0.003,
    requires_external_provider=True,
)


def choose_model_route(constraints: RouteConstraints) -> RouteDecision:
    """Choose a route without calling any external provider."""

    if not constraints.provider_budget_approved:
        return RouteDecision(
            selected_route=asdict(LOCAL_BASELINE),
            fallback_route=asdict(LOCAL_BASELINE),
            reason="provider budget is not approved; use local deterministic baseline",
            provider_call_made=False,
        )

    if (
        constraints.severity == "high"
        and constraints.latency_budget_ms >= STRONG_EXTERNAL.estimated_latency_ms
        and constraints.max_cost_usd >= STRONG_EXTERNAL.estimated_cost_usd
    ):
        return RouteDecision(
            selected_route=asdict(STRONG_EXTERNAL),
            fallback_route=asdict(FAST_EXTERNAL),
            reason="high severity with enough latency and cost budget for stronger analysis",
            provider_call_made=False,
        )

    if (
        constraints.latency_budget_ms >= FAST_EXTERNAL.estimated_latency_ms
        and constraints.max_cost_usd >= FAST_EXTERNAL.estimated_cost_usd
    ):
        return RouteDecision(
            selected_route=asdict(FAST_EXTERNAL),
            fallback_route=asdict(LOCAL_BASELINE),
            reason="budget allows fast external route, but this lesson still performs no call",
            provider_call_made=False,
        )

    return RouteDecision(
        selected_route=asdict(LOCAL_BASELINE),
        fallback_route=asdict(LOCAL_BASELINE),
        reason="latency or cost budget is too small for external routing",
        provider_call_made=False,
    )
