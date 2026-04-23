"""跨步骤共享数据存储，用于在业务流各步骤间传递运行时数据。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SharedStore:
    """基于字典的轻量级键值存储，供业务流步骤间共享运行时数据（如订单号、SKU）。"""

    payload: dict[str, Any] = field(default_factory=dict)

    def put(self, key: str, value: Any) -> None:
        """将键值对写入共享存储。"""
        self.payload[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """按键读取共享数据，键不存在时返回默认值。"""
        return self.payload.get(key, default)