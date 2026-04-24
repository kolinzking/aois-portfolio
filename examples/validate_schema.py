#!/usr/bin/env python3
"""Validate the Phase 0 v0.8 SQL schema without connecting to a database."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_SNIPPETS = {
    "portfolio_schema": "create schema if not exists aois_p",
    "incidents_table": "create table if not exists aois_p.incidents",
    "analysis_results_table": "create table if not exists aois_p.analysis_results",
    "llm_request_plans_table": "create table if not exists aois_p.llm_request_plans",
    "incident_message_check": "message text not null check (length(trim(message)) > 0)",
    "incident_status_check": "check (status in ('new', 'analyzed', 'archived'))",
    "analysis_incident_fk": "references aois_p.incidents(id) on delete cascade",
    "analysis_confidence_check": "check (confidence >= 0 and confidence <= 1)",
    "llm_provider_gate": "provider_call_allowed boolean not null default false",
    "llm_token_budget_check": "max_output_tokens integer not null check (max_output_tokens > 0)",
}


def normalize_sql(sql: str) -> str:
    without_comments = re.sub(r"--.*", "", sql)
    return re.sub(r"\s+", " ", without_comments.lower()).strip()


def validate_schema(path: Path) -> dict[str, object]:
    sql = path.read_text(encoding="utf-8")
    normalized = normalize_sql(sql)
    missing = [
        name
        for name, required in REQUIRED_SNIPPETS.items()
        if required not in normalized
    ]
    return {
        "schema_path": str(path),
        "required_checks": len(REQUIRED_SNIPPETS),
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate required AOIS portfolio schema patterns."
    )
    parser.add_argument(
        "schema",
        nargs="?",
        default="sql/aois_schema.sql",
        help="Path to the SQL schema file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    path = Path(args.schema)
    if not path.exists():
        parser.error(f"schema file does not exist: {path}")

    result = validate_schema(path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
