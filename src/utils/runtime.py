"""运行时工具函数，提供环境检测和运行标识生成。"""

from __future__ import annotations

import os
from datetime import datetime


def is_live_ui_enabled() -> bool:
    """检查环境变量 ENABLE_LIVE_UI 是否为 true，决定是否执行真实 UI 用例。"""
    return os.getenv("ENABLE_LIVE_UI", "false").lower() == "true"


def build_run_id(prefix: str = "run") -> str:
    """生成带时间戳的运行标识，用于区分不同批次的执行。"""
    return f"{prefix}-{datetime.now():%Y%m%d%H%M%S}"