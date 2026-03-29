from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ExecutionReportCollector:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.records: list[dict[str, Any]] = []

    def add_record(self, payload: dict[str, Any]) -> None:
        self.records.append(payload)

    def flush(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(self.records, ensure_ascii=False, indent=2), encoding="utf-8")