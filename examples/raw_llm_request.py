#!/usr/bin/env python3
"""Dry-run raw LLM request builder for Phase 0 v0.7.

This file intentionally does not call an external provider.
It teaches request shape, token/cost estimation, latency budgeting, and
structured-output expectations before any API key is introduced.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import asdict, dataclass


APPROX_CHARS_PER_TOKEN = 4


@dataclass(frozen=True)
class LLMRequestDraft:
    """Provider-neutral request draft."""

    model: str
    system_prompt: str
    user_prompt: str
    temperature: float
    response_format: str


@dataclass(frozen=True)
class LLMRequestEstimate:
    """Local estimate for a request before sending it to a provider."""

    input_tokens_estimate: int
    max_output_tokens: int
    estimated_total_tokens: int
    estimated_cost_usd: float
    latency_budget_ms: int


def estimate_tokens(text: str) -> int:
    """Estimate token count without provider-specific tokenization."""

    stripped = text.strip()
    if not stripped:
        return 0
    return max(1, math.ceil(len(stripped) / APPROX_CHARS_PER_TOKEN))


def estimate_request(
    draft: LLMRequestDraft,
    max_output_tokens: int,
    cost_per_million_tokens: float,
    latency_budget_ms: int,
) -> LLMRequestEstimate:
    input_tokens = estimate_tokens(draft.system_prompt) + estimate_tokens(draft.user_prompt)
    total_tokens = input_tokens + max_output_tokens
    estimated_cost = (total_tokens / 1_000_000) * cost_per_million_tokens
    return LLMRequestEstimate(
        input_tokens_estimate=input_tokens,
        max_output_tokens=max_output_tokens,
        estimated_total_tokens=total_tokens,
        estimated_cost_usd=estimated_cost,
        latency_budget_ms=latency_budget_ms,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a dry-run LLM request.")
    parser.add_argument("message", nargs="+", help="Incident message to analyze.")
    parser.add_argument("--model", default="provider-model-placeholder")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-output-tokens", type=int, default=300)
    parser.add_argument("--cost-per-million-tokens", type=float, default=1.00)
    parser.add_argument("--latency-budget-ms", type=int, default=2000)
    parser.add_argument("--format", default="json_object", choices=["text", "json_object"])
    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.max_output_tokens < 1:
        parser.error("--max-output-tokens must be at least 1")
    if args.cost_per_million_tokens < 0:
        parser.error("--cost-per-million-tokens cannot be negative")
    if args.latency_budget_ms < 1:
        parser.error("--latency-budget-ms must be at least 1")
    if not 0 <= args.temperature <= 2:
        parser.error("--temperature must be between 0 and 2 for this dry-run lesson")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    validate_args(parser, args)

    incident = " ".join(args.message)
    draft = LLMRequestDraft(
        model=args.model,
        system_prompt=(
            "You are AOIS, an operations analysis assistant. "
            "Return concise, structured incident analysis."
        ),
        user_prompt=f"Analyze this incident signal: {incident}",
        temperature=args.temperature,
        response_format=args.format,
    )
    estimate = estimate_request(
        draft=draft,
        max_output_tokens=args.max_output_tokens,
        cost_per_million_tokens=args.cost_per_million_tokens,
        latency_budget_ms=args.latency_budget_ms,
    )

    output = {
        "mode": "dry_run_no_provider_call",
        "request": asdict(draft),
        "estimate": asdict(estimate),
        "expected_structured_fields": [
            "category",
            "severity",
            "confidence",
            "summary",
            "recommended_action",
        ],
        "created_at_unix": int(time.time()),
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
