"""WMS 仓储领域数据模型，定义库存记录等业务实体。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InventoryRecord:
    """库存记录，表示某仓库中某 SKU 的当前库存数量。"""

    sku_code: str  # 中文说明：商品 SKU 编码
    quantity: int  # 中文说明：库存数量
    warehouse_code: str = "MAIN"  # 中文说明：仓库编码，默认主仓