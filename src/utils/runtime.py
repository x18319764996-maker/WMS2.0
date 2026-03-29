"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

import os
from datetime import datetime


def is_live_ui_enabled() -> bool:
    """中文说明：判断与 is_live_ui_enabled 相关的逻辑。"""
    return os.getenv("ENABLE_LIVE_UI", "false").lower() == "true"


def build_run_id(prefix: str = "run") -> str:
    """中文说明：构建与 build_run_id 相关的逻辑。"""
    return f"{prefix}-{datetime.now():%Y%m%d%H%M%S}"