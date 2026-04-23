"""OMS API 客户端，封装订单查询和搜索等接口调用。"""

from __future__ import annotations

from api.base_client import ApiClient
from core.config.models import ApiSettings, SystemEndpoint


class OMSApiClient(ApiClient):
    """OMS 专用 API 客户端，自动绑定 OMS 接口路径模板。"""

    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings) -> None:
        """注入 OMS 系统端点和 API 配置，使用 oms_endpoints 路径模板。"""
        super().__init__(system_config, api_settings, api_settings.oms_endpoints)

    def get_order_detail(self, order_no: str) -> dict:
        """按订单号查询订单详情。"""
        return self.get("order_detail", order_no=order_no).json()

    def search_order(self, keyword: str) -> dict:
        """按关键字搜索订单列表。"""
        return self.get("order_search", params={"keyword": keyword}).json()