#!/usr/bin/env python3
"""Validate Phase 3 v6 Kubernetes manifests without applying them."""

from __future__ import annotations

import json
from pathlib import Path


MANIFEST_DIR = Path("k8s/aois-p")
REQUIRED_FILES = [
    "namespace.yaml",
    "resource-quota.yaml",
    "limit-range.yaml",
    "deployment.yaml",
    "service.yaml",
    "kustomization.yaml",
]

REQUIRED_SNIPPETS = {
    "namespace_name": ("namespace.yaml", "name: aois-p"),
    "quota_cpu_limit": ("resource-quota.yaml", 'limits.cpu: "500m"'),
    "quota_memory_limit": ("resource-quota.yaml", 'limits.memory: "512Mi"'),
    "limit_range": ("limit-range.yaml", "kind: LimitRange"),
    "deployment_name": ("deployment.yaml", "name: aois-p-api"),
    "deployment_namespace": ("deployment.yaml", "namespace: aois-p"),
    "single_replica": ("deployment.yaml", "replicas: 1"),
    "provider_disabled": ("deployment.yaml", "AOIS_PROVIDER_CALLS_ENABLED"),
    "cpu_limit": ("deployment.yaml", 'cpu: "250m"'),
    "memory_limit": ("deployment.yaml", 'memory: "256Mi"'),
    "readiness_probe": ("deployment.yaml", "readinessProbe:"),
    "non_root": ("deployment.yaml", "runAsNonRoot: true"),
    "service_cluster_ip": ("service.yaml", "type: ClusterIP"),
    "kustomization": ("kustomization.yaml", "kind: Kustomization"),
}


def validate_k8s_plan() -> dict[str, object]:
    missing: list[str] = []

    for filename in REQUIRED_FILES:
        if not (MANIFEST_DIR / filename).exists():
            missing.append(f"missing_file:{filename}")

    for name, (filename, snippet) in REQUIRED_SNIPPETS.items():
        path = MANIFEST_DIR / filename
        if path.exists() and snippet not in path.read_text(encoding="utf-8"):
            missing.append(f"{filename}:{name}")

    return {
        "mode": "kubernetes_plan_validation_no_apply",
        "kubectl_apply_ran": False,
        "namespace": "aois-p",
        "required_files": REQUIRED_FILES,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_k8s_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
