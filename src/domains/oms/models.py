from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OMSOrder:
    order_no: str
    customer_name: str
    sku_code: str
    quantity: int
    status: str = "draft"