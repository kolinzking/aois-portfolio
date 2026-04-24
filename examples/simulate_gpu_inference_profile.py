#!/usr/bin/env python3
"""Simulate a Phase 5 v13 GPU inference profile without GPU runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/gpu-inference-service.plan.json")


def estimate_tokens(text: str) -> int:
    # This is deliberately simple; the lesson is about contracts, not tokenizers.
    return max(1, len(text.split()))


def build_profile() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    prompt = "AOIS incident: gateway latency increased after model route change"
    tokens_in = estimate_tokens(prompt)
    tokens_out = min(64, int(tokens_in * 1.5) + 8)
    latency_ms = plan["performance_budget"]["target_p50_latency_ms"]

    return {
        "mode": "gpu_inference_profile_simulation_no_runtime",
        "gpu_runtime_started": False,
        "model_downloaded": False,
        "request": {
            "trace_id": "trace-v13-local-sim",
            "model_route": "aois-p-gpu-inference-placeholder",
            "prompt": prompt,
            "max_tokens": 64,
            "temperature": 0.2,
        },
        "response": {
            "trace_id": "trace-v13-local-sim",
            "model_route": "aois-p-gpu-inference-placeholder",
            "output": "Simulated GPU inference response for contract practice.",
            "latency_ms": latency_ms,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "backend_metadata": {
                "backend": "no-runtime-simulation",
                "serving_options_considered": [
                    option["name"] for option in plan["serving_options"]
                ],
            },
        },
        "status": "pass",
    }


def main() -> int:
    print(json.dumps(build_profile(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
