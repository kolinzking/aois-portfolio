#!/usr/bin/env python3
"""Validate the Phase 2 v4 container plan without building an image."""

from __future__ import annotations

import json
import re
from pathlib import Path


REQUIRED_FILES = [
    Path("Dockerfile"),
    Path(".dockerignore"),
    Path("compose.yaml"),
]

REQUIRED_DOCKERFILE_SNIPPETS = {
    "python_slim_base": "FROM python:3.12-slim",
    "non_root_user": "USER aois",
    "no_cache_install": "pip install --no-cache-dir -r requirements.txt",
    "healthcheck": "HEALTHCHECK",
    "uvicorn_cmd": 'CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8006"]',
}

REQUIRED_COMPOSE_SNIPPETS = {
    "portfolio_service_name": "aois-p-api:",
    "portfolio_image_name": "image: aois-p/api:local",
    "localhost_port_binding": '"127.0.0.1:8006:8006"',
    "memory_limit": "mem_limit: 256m",
    "cpu_limit": 'cpus: "0.50"',
    "read_only_filesystem": "read_only: true",
    "no_restart_policy": 'restart: "no"',
}

REQUIRED_DOCKERIGNORE_LINES = {
    ".git",
    ".venv",
    "__pycache__",
    ".env",
    "curriculum",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def validate_container_plan() -> dict[str, object]:
    missing: list[str] = []

    for path in REQUIRED_FILES:
        if not path.exists():
            missing.append(f"missing_file:{path}")

    if Path("Dockerfile").exists():
        dockerfile = normalize(Path("Dockerfile").read_text(encoding="utf-8"))
        for name, snippet in REQUIRED_DOCKERFILE_SNIPPETS.items():
            if snippet not in dockerfile:
                missing.append(f"dockerfile:{name}")

    if Path("compose.yaml").exists():
        compose = Path("compose.yaml").read_text(encoding="utf-8")
        for name, snippet in REQUIRED_COMPOSE_SNIPPETS.items():
            if snippet not in compose:
                missing.append(f"compose:{name}")

    if Path(".dockerignore").exists():
        ignored = {
            line.strip()
            for line in Path(".dockerignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        }
        for required in REQUIRED_DOCKERIGNORE_LINES:
            if required not in ignored:
                missing.append(f"dockerignore:{required}")

    return {
        "mode": "container_plan_validation_no_build",
        "provider_call_made": False,
        "docker_build_ran": False,
        "required_files": [str(path) for path in REQUIRED_FILES],
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def main() -> int:
    result = validate_container_plan()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
