"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


class TestDataLoader:
    def __init__(self, data_root: Path | None = None) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.data_root = data_root or Path(__file__).resolve().parent / "testdata"

    def load_yaml(self, relative_path: str) -> dict[str, Any]:
        """中文说明：在 TestDataLoader 中加载与 load_yaml 相关的操作。"""
        path = self.data_root / relative_path
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def load_json(self, relative_path: str) -> dict[str, Any]:
        """中文说明：在 TestDataLoader 中加载与 load_json 相关的操作。"""
        path = self.data_root / relative_path
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)