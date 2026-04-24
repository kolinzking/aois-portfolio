#!/usr/bin/env python3
"""Run the Phase 0 Python incident analyzer from the terminal."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.analysis import analyze_incident
from app.models import IncidentInput


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze an AOIS incident message.")
    parser.add_argument("message", nargs="+", help="Raw incident message to classify.")
    parser.add_argument("--source", default="manual", help="Where the message came from.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    incident = IncidentInput(message=" ".join(args.message), source=args.source)
    result = analyze_incident(incident)

    print(f"category={result.category}")
    print(f"severity={result.severity.value}")
    print(f"confidence={result.confidence:.2f}")
    print(f"summary={result.summary}")
    print(f"recommended_action={result.recommended_action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
