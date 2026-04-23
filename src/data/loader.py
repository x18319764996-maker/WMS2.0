"""测试数据加载器，从 YAML 和 JSON 文件读取外部测试数据。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


class TestDataLoader:
    """测试数据加载器，按相对路径从数据根目录加载 YAML 或 JSON 文件。"""

    def __init__(self, data_root: Path | None = None) -> None:
        """注入数据根目录；默认为本模块同级的 testdata 目录。"""
        self.data_root = data_root or Path(__file__).resolve().parent / "testdata"

    def load_yaml(self, relative_path: str) -> dict[str, Any]:
        """加载指定相对路径的 YAML 文件并返回字典。"""
        path = self.data_root / relative_path
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def load_json(self, relative_path: str) -> dict[str, Any]:
        """加载指定相对路径的 JSON 文件并返回字典。"""
        path = self.data_root / relative_path
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)