#!/usr/bin/env python3
"""Simulate Phase 5 v15 base-vs-adapted eval without training."""

from __future__ import annotations

import json


CASES = [
    {
        "name": "gateway_regression",
        "base_pass": True,
        "adapted_candidate_pass": True,
    },
    {
        "name": "gpu_memory_pressure",
        "base_pass": False,
        "adapted_candidate_pass": True,
    },
    {
        "name": "cache_staleness",
        "base_pass": True,
        "adapted_candidate_pass": True,
    },
    {
        "name": "ambiguous_operator_request",
        "base_pass": True,
        "adapted_candidate_pass": False,
    },
]


def score(key: str) -> float:
    passed = sum(1 for case in CASES if case[key])
    return passed / len(CASES)


def simulate_adaptation_eval() -> dict[str, object]:
    base_score = score("base_pass")
    adapted_score = score("adapted_candidate_pass")
    regression_count = sum(
        1
        for case in CASES
        if case["base_pass"] and not case["adapted_candidate_pass"]
    )

    return {
        "mode": "adaptation_eval_simulation_no_training",
        "training_job_started": False,
        "dataset_uploaded": False,
        "model_downloaded": False,
        "base_score": base_score,
        "adapted_candidate_score": adapted_score,
        "regression_count": regression_count,
        "recommendation": "do_not_train_until_regressions_are_resolved",
        "cases": CASES,
        "status": "pass",
    }


def main() -> int:
    print(json.dumps(simulate_adaptation_eval(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
