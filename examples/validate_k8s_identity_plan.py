#!/usr/bin/env python3
"""Validate Phase 3 v6.5 identity manifests without applying them."""

from __future__ import annotations

import json
from pathlib import Path


MANIFEST_DIR = Path("k8s/aois-p")

REQUIRED_SNIPPETS = {
    "service_account": ("service-account.yaml", "kind: ServiceAccount"),
    "service_account_name": ("service-account.yaml", "name: aois-p-api"),
    "token_disabled": ("service-account.yaml", "automountServiceAccountToken: false"),
    "deployment_service_account": ("deployment.yaml", "serviceAccountName: aois-p-api"),
    "deployment_token_disabled": ("deployment.yaml", "automountServiceAccountToken: false"),
    "minimal_role": ("role.yaml", "rules: []"),
    "role_binding": ("role-binding.yaml", "kind: RoleBinding"),
    "network_policy": ("network-policy.yaml", "kind: NetworkPolicy"),
    "egress_denied": ("network-policy.yaml", "egress: []"),
    "kustomization_service_account": ("kustomization.yaml", "service-account.yaml"),
    "kustomization_network_policy": ("kustomization.yaml", "network-policy.yaml"),
}


def validate_identity_plan() -> dict[str, object]:
    missing: list[str] = []
    for name, (filename, snippet) in REQUIRED_SNIPPETS.items():
        path = MANIFEST_DIR / filename
        if not path.exists():
            missing.append(f"missing_file:{filename}")
            continue
        if snippet not in path.read_text(encoding="utf-8"):
            missing.append(f"{filename}:{name}")

    return {
        "mode": "kubernetes_identity_validation_no_apply",
        "kubectl_apply_ran": False,
        "namespace": "aois-p",
        "service_account": "aois-p-api",
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_identity_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
