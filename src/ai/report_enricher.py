from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ReportEnricher:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def write_summary(self, payload: dict[str, Any]) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")