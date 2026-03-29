from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InventoryRecord:
    sku_code: str
    quantity: int
    warehouse_code: str = "MAIN"