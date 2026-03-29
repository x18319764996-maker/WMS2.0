"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CrossSystemOrderContext:
    order_no: str = ""
    receipt_no: str = ""
    outbound_no: str = ""
    sku_code: str = ""