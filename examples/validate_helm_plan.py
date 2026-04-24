#!/usr/bin/env python3
"""Validate Phase 3 v7 Helm chart files without installing a release."""

from __future__ import annotations

import json
from pathlib import Path


CHART_DIR = Path("charts/aois-p")
REQUIRED_FILES = [
    "Chart.yaml",
    "values.yaml",
    "templates/namespace.yaml",
    "templates/resource-quota.yaml",
    "templates/service-account.yaml",
    "templates/deployment.yaml",
    "templates/service.yaml",
    "templates/network-policy.yaml",
]

REQUIRED_SNIPPETS = {
    "chart_name": ("Chart.yaml", "name: aois-p"),
    "namespace_value": ("values.yaml", "namespace: aois-p"),
    "replica_value": ("values.yaml", "replicas: 1"),
    "provider_disabled": ("values.yaml", 'providerCallsEnabled: "false"'),
    "cpu_limit": ("values.yaml", "cpu: 250m"),
    "memory_limit": ("values.yaml", "memory: 256Mi"),
    "namespace_template": ("templates/namespace.yaml", "{{ .Values.namespace }}"),
    "quota_template": ("templates/resource-quota.yaml", "kind: ResourceQuota"),
    "service_account_template": ("templates/service-account.yaml", "kind: ServiceAccount"),
    "deployment_service_account": ("templates/deployment.yaml", "serviceAccountName: {{ .Values.app.name }}"),
    "deployment_provider_gate": ("templates/deployment.yaml", "AOIS_PROVIDER_CALLS_ENABLED"),
    "service_cluster_ip": ("templates/service.yaml", "type: {{ .Values.service.type }}"),
    "network_policy": ("templates/network-policy.yaml", "kind: NetworkPolicy"),
    "egress_denied": ("templates/network-policy.yaml", "egress: []"),
}


def validate_helm_plan() -> dict[str, object]:
    missing: list[str] = []
    for filename in REQUIRED_FILES:
        if not (CHART_DIR / filename).exists():
            missing.append(f"missing_file:{filename}")

    for name, (filename, snippet) in REQUIRED_SNIPPETS.items():
        path = CHART_DIR / filename
        if path.exists() and snippet not in path.read_text(encoding="utf-8"):
            missing.append(f"{filename}:{name}")

    return {
        "mode": "helm_chart_validation_no_install",
        "helm_install_ran": False,
        "chart": "aois-p",
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_helm_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
