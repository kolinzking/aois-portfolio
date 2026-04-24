#!/usr/bin/env python3
"""Run the Phase 1 v3 local evaluation baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.reliability import run_eval_baseline


def main() -> int:
    result = run_eval_baseline()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["score"] == 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
