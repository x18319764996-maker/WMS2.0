from __future__ import annotations

import os
from datetime import datetime


def is_live_ui_enabled() -> bool:
    return os.getenv("ENABLE_LIVE_UI", "false").lower() == "true"


def build_run_id(prefix: str = "run") -> str:
    return f"{prefix}-{datetime.now():%Y%m%d%H%M%S}"