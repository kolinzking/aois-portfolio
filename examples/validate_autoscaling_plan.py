#!/usr/bin/env python3
"""Validate Phase 3 v9 autoscaling plan without applying resources."""

from __future__ import annotations

import json
from pathlib import Path


MANIFEST_DIR = Path("k8s/aois-p")

REQUIRED_SNIPPETS = {
    "hpa_kind": ("hpa.yaml", "kind: HorizontalPodAutoscaler"),
    "hpa_namespace": ("hpa.yaml", "namespace: aois-p"),
    "hpa_target": ("hpa.yaml", "name: aois-p-api"),
    "hpa_min_one": ("hpa.yaml", "minReplicas: 1"),
    "hpa_max_one": ("hpa.yaml", "maxReplicas: 1"),
    "hpa_cpu_metric": ("hpa.yaml", "averageUtilization: 70"),
    "keda_plan_kind": ("keda-scaledobject.plan.yaml", "kind: ScaledObject"),
    "keda_max_one": ("keda-scaledobject.plan.yaml", "maxReplicaCount: 1"),
    "keda_cpu_trigger": ("keda-scaledobject.plan.yaml", "type: cpu"),
    "kustomization_hpa": ("kustomization.yaml", "hpa.yaml"),
}


def validate_autoscaling_plan() -> dict[str, object]:
    missing: list[str] = []
    for name, (filename, snippet) in REQUIRED_SNIPPETS.items():
        path = MANIFEST_DIR / filename
        if not path.exists():
            missing.append(f"missing_file:{filename}")
            continue
        if snippet not in path.read_text(encoding="utf-8"):
            missing.append(f"{filename}:{name}")

    return {
        "mode": "autoscaling_plan_validation_no_apply",
        "kubectl_apply_ran": False,
        "keda_installed": False,
        "max_replicas": 1,
        "namespace": "aois-p",
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_autoscaling_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
