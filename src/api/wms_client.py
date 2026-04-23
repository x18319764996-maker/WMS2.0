"""WMS API 客户端，封装入库、库存和出库等仓储接口调用。"""

from __future__ import annotations

from api.base_client import ApiClient
from core.config.models import ApiSettings, SystemEndpoint


class WMSApiClient(ApiClient):
    """WMS 专用 API 客户端，自动绑定 WMS 接口路径模板。"""

    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings) -> None:
        """注入 WMS 系统端点和 API 配置，使用 wms_endpoints 路径模板。"""
        super().__init__(system_config, api_settings, api_settings.wms_endpoints)

    def get_inbound_detail(self, receipt_no: str) -> dict:
        """按入库单号查询入库明细。"""
        return self.get("inbound_detail", receipt_no=receipt_no).json()

    def query_inventory(self, sku_code: str) -> dict:
        """按 SKU 编码查询当前库存。"""
        return self.get("inventory_query", params={"sku_code": sku_code}).json()

    def get_outbound_detail(self, outbound_no: str) -> dict:
        """按出库单号查询出库明细。"""
        return self.get("outbound_detail", outbound_no=outbound_no).json()