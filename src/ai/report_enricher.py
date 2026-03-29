"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ReportEnricher:
    def __init__(self, output_path: Path) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.output_path = output_path

    def write_summary(self, payload: dict[str, Any]) -> None:
        """中文说明：在 ReportEnricher 中写入与 write_summary 相关的操作。"""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")