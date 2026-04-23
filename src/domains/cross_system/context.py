"""跨系统联动上下文，在 OMS→WMS 端到端流程中传递共享业务数据。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CrossSystemOrderContext:
    """OMS 与 WMS 跨系统流程的共享上下文，在各步骤间传递单据编号和商品信息。"""

    order_no: str = ""  # 中文说明：OMS 订单编号
    receipt_no: str = ""  # 中文说明：WMS 入库单号
    outbound_no: str = ""  # 中文说明：WMS 出库单号
    sku_code: str = ""  # 中文说明：商品 SKU 编码