#!/usr/bin/env python3
"""Run Phase 2 v5 local security inspection from the terminal."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.security import inspect_security


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect an AOIS message for local security risks.")
    parser.add_argument("message", nargs="+", help="Message to inspect.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    result = inspect_security(" ".join(args.message))
    print(json.dumps(asdict(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
