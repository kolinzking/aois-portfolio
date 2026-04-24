#!/usr/bin/env python3
"""Validate Phase 3 v8 GitOps plan without applying it."""

from __future__ import annotations

import json
from pathlib import Path


APP_PATH = Path("gitops/argocd/aois-p-application.yaml")
README_PATH = Path("gitops/argocd/README.md")

REQUIRED_SNIPPETS = {
    "argocd_application": (APP_PATH, "kind: Application"),
    "app_name": (APP_PATH, "name: aois-p"),
    "argocd_namespace": (APP_PATH, "namespace: argocd"),
    "chart_path": (APP_PATH, "path: charts/aois-p"),
    "target_namespace": (APP_PATH, "namespace: aois-p"),
    "automated_disabled": (APP_PATH, "automated: null"),
    "no_create_namespace": (APP_PATH, "CreateNamespace=false"),
    "revision_history": (APP_PATH, "revisionHistoryLimit: 3"),
    "readme_no_apply": (README_PATH, "no `kubectl apply`"),
    "readme_no_sync": (README_PATH, "no cluster sync"),
}


def validate_gitops_plan() -> dict[str, object]:
    missing: list[str] = []
    for name, (path, snippet) in REQUIRED_SNIPPETS.items():
        if not path.exists():
            missing.append(f"missing_file:{path}")
            continue
        if snippet not in path.read_text(encoding="utf-8"):
            missing.append(f"{path}:{name}")

    return {
        "mode": "gitops_plan_validation_no_apply",
        "kubectl_apply_ran": False,
        "argocd_sync_ran": False,
        "application": "aois-p",
        "target_namespace": "aois-p",
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_gitops_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
