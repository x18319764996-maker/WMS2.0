from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SharedStore:
    payload: dict[str, Any] = field(default_factory=dict)

    def put(self, key: str, value: Any) -> None:
        self.payload[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.payload.get(key, default)