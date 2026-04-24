"""Configuration helpers for local AOIS development."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Small settings object before external config libraries are introduced."""

    app_name: str = "aois"
    environment: str = "local"


def load_settings() -> Settings:
    """Load settings from environment variables with safe local defaults."""

    return Settings(
        app_name=os.getenv("AOIS_APP_NAME", "aois"),
        environment=os.getenv("AOIS_ENV", "local"),
    )
