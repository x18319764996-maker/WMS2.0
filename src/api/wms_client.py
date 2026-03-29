"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from api.base_client import ApiClient
from core.config.models import ApiSettings, SystemEndpoint


class WMSApiClient(ApiClient):
    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(system_config, api_settings, api_settings.wms_endpoints)

    def get_inbound_detail(self, receipt_no: str) -> dict:
        """中文说明：在 WMSApiClient 中获取与 get_inbound_detail 相关的操作。"""
        return self.get("inbound_detail", receipt_no=receipt_no).json()

    def query_inventory(self, sku_code: str) -> dict:
        """中文说明：在 WMSApiClient 中查询与 query_inventory 相关的操作。"""
        return self.get("inventory_query", params={"sku_code": sku_code}).json()

    def get_outbound_detail(self, outbound_no: str) -> dict:
        """中文说明：在 WMSApiClient 中获取与 get_outbound_detail 相关的操作。"""
        return self.get("outbound_detail", outbound_no=outbound_no).json()