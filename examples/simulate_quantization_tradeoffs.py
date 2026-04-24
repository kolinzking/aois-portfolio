#!/usr/bin/env python3
"""Simulate Phase 5 v15.5 quantization tradeoffs without runtime."""

from __future__ import annotations

import json
from pathlib import Path


PLAN_PATH = Path("inference/aois-p/quantization-memory.plan.json")


def simulate_quantization() -> dict[str, object]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    baseline = plan["precision_options"][0]
    baseline_memory = baseline["simulated_memory_gb"]
    baseline_quality = baseline["simulated_quality_score"]

    options = []
    for option in plan["precision_options"]:
        memory = option["simulated_memory_gb"]
        quality = option["simulated_quality_score"]
        options.append(
            {
                "name": option["name"],
                "weight_bits": option["weight_bits"],
                "simulated_memory_gb": memory,
                "simulated_speed_index": option["simulated_speed_index"],
                "simulated_quality_score": quality,
                "memory_reduction_vs_fp16": round((baseline_memory - memory) / baseline_memory, 2),
                "quality_delta_vs_fp16": round(quality - baseline_quality, 2),
                "live_use_approved": option["live_use_approved"],
            }
        )

    return {
        "mode": "quantization_tradeoff_simulation_no_runtime",
        "quantization_job_started": False,
        "model_downloaded": False,
        "gpu_runtime_started": False,
        "options": options,
        "status": "pass",
    }


def main() -> int:
    print(json.dumps(simulate_quantization(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
