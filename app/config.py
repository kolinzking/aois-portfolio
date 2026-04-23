from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


def get_settings() -> dict[str, str]:
    return {
        "app_name": os.getenv("AOIS_APP_NAME", "aois-phase0"),
        "environment": os.getenv("AOIS_ENV", "dev"),
        "anthropic_api_key_present": "yes" if os.getenv("ANTHROPIC_API_KEY") else "no",
        "database_url_present": "yes" if os.getenv("DATABASE_URL") else "no",
    }
