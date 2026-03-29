"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SharedStore:
    payload: dict[str, Any] = field(default_factory=dict)

    def put(self, key: str, value: Any) -> None:
        """中文说明：在 SharedStore 中写入共享数据与 put 相关的操作。"""
        self.payload[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """中文说明：在 SharedStore 中获取与 get 相关的操作。"""
        return self.payload.get(key, default)