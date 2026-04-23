"""报告增强模块，将 AI 决策摘要写入独立 JSON 文件供后续分析。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ReportEnricher:
    """报告增强器，将 AI 相关的执行摘要序列化输出到指定文件。"""

    def __init__(self, output_path: Path) -> None:
        """注入摘要输出文件路径。"""
        self.output_path = output_path

    def write_summary(self, payload: dict[str, Any]) -> None:
        """将 AI 决策摘要序列化为 JSON 并写入文件。"""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")