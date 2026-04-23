"""OMS 订单领域数据模型，定义订单实体及其状态流转。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OMSOrder:
    """OMS 订单实体，承载订单号、客户、商品和状态等核心业务字段。"""

    order_no: str  # 中文说明：订单编号
    customer_name: str  # 中文说明：客户名称
    sku_code: str  # 中文说明：商品 SKU 编码
    quantity: int  # 中文说明：订购数量
    status: str = "draft"  # 中文说明：订单状态，初始为 draft（草稿）