"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from api.base_client import ApiClient
from core.config.models import ApiSettings, SystemEndpoint


class OMSApiClient(ApiClient):
    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(system_config, api_settings, api_settings.oms_endpoints)

    def get_order_detail(self, order_no: str) -> dict:
        """中文说明：在 OMSApiClient 中获取与 get_order_detail 相关的操作。"""
        return self.get("order_detail", order_no=order_no).json()

    def search_order(self, keyword: str) -> dict:
        """中文说明：在 OMSApiClient 中查询与 search_order 相关的操作。"""
        return self.get("order_search", params={"keyword": keyword}).json()