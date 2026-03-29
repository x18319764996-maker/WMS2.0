from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CrossSystemOrderContext:
    order_no: str = ""
    receipt_no: str = ""
    outbound_no: str = ""
    sku_code: str = ""