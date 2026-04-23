"""执行报告收集器，在内存中累积执行记录并一次性落盘为 JSON 文件。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ExecutionReportCollector:
    """执行报告收集器，按步骤收集执行记录，在测试结束后统一序列化输出。"""

    def __init__(self, output_path: Path) -> None:
        """注入报告输出文件路径，并初始化空记录列表。"""
        self.output_path = output_path
        self.records: list[dict[str, Any]] = []

    def add_record(self, payload: dict[str, Any]) -> None:
        """追加一条执行记录到内存列表，等待 flush 时统一落盘。"""
        self.records.append(payload)

    def flush(self) -> None:
        """将内存中所有执行记录序列化为 JSON 并写入文件。"""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(self.records, ensure_ascii=False, indent=2), encoding="utf-8")