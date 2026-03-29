from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


class TestDataLoader:
    def __init__(self, data_root: Path | None = None) -> None:
        self.data_root = data_root or Path(__file__).resolve().parent / "testdata"

    def load_yaml(self, relative_path: str) -> dict[str, Any]:
        path = self.data_root / relative_path
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def load_json(self, relative_path: str) -> dict[str, Any]:
        path = self.data_root / relative_path
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)