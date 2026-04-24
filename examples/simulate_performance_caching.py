#!/usr/bin/env python3
"""Simulate Phase 5 v14.5 caching tradeoffs without cache runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/performance-caching.plan.json")


def simulate_caching() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    baseline = plan["cache_layers"][0]
    baseline_latency = baseline["simulated_latency_ms"]
    baseline_tokens = baseline["simulated_tokens_billed"]

    layers = []
    for layer in plan["cache_layers"]:
        latency = layer["simulated_latency_ms"]
        tokens = layer["simulated_tokens_billed"]
        layers.append(
            {
                "name": layer["name"],
                "cache_type": layer["cache_type"],
                "simulated_hit_rate": layer["simulated_hit_rate"],
                "simulated_latency_ms": latency,
                "simulated_tokens_billed": tokens,
                "latency_gain_vs_no_cache": round(baseline_latency / latency, 2),
                "token_reduction_vs_no_cache": round(
                    (baseline_tokens - tokens) / baseline_tokens,
                    2,
                ),
                "live_use_approved": layer["live_use_approved"],
            }
        )

    return {
        "mode": "performance_caching_simulation_no_runtime",
        "cache_service_started": False,
        "redis_installed": False,
        "cache_entries_created": False,
        "layers": layers,
        "status": "pass",
    }


def main() -> int:
    print(json.dumps(simulate_caching(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
