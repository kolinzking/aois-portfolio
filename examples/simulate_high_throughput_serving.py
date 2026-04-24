#!/usr/bin/env python3
"""Simulate Phase 5 v14 serving throughput modes without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/high-throughput-serving.plan.json")


def compare_modes() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    modes = []
    baseline_tps = plan["serving_modes"][0]["simulated_tokens_per_second"]

    for mode in plan["serving_modes"]:
        tokens_per_second = mode["simulated_tokens_per_second"]
        modes.append(
            {
                "name": mode["name"],
                "batch_size": mode["batch_size"],
                "max_concurrency": mode["max_concurrency"],
                "simulated_tokens_per_second": tokens_per_second,
                "simulated_p95_latency_ms": mode["simulated_p95_latency_ms"],
                "throughput_gain_vs_serial": round(tokens_per_second / baseline_tps, 2),
                "live_use_approved": mode["live_use_approved"],
            }
        )

    return {
        "mode": "high_throughput_serving_simulation_no_runtime",
        "inference_runtime_started": False,
        "gpu_runtime_started": False,
        "model_downloaded": False,
        "modes": modes,
        "status": "pass",
    }


def main() -> int:
    print(json.dumps(compare_modes(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
