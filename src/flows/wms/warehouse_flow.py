"""WMS 仓储业务流，串联登录→入库→库存查询→出库的完整作业链路。"""

from __future__ import annotations

from api.wms_client import WMSApiClient
from flows.base_flow import BaseFlow
from pages.wms.inbound_page import WMSInboundPage
from pages.wms.inventory_page import WMSInventoryPage
from pages.wms.login_page import WMSLoginPage
from pages.wms.outbound_page import WMSOutboundPage


class WMSWarehouseFlow(BaseFlow):
    """WMS 仓储核心业务流，组合 4 个 WMS 页面对象和 API 客户端，提供入库、出库、库存查询等端到端编排。"""

    def __init__(self, login_page: WMSLoginPage, inbound_page: WMSInboundPage, inventory_page: WMSInventoryPage, outbound_page: WMSOutboundPage, api_client: WMSApiClient, assertion_assistant, failure_analysis_agent) -> None:
        """注入登录页、入库页、库存页、出库页、API 客户端和 AI 辅助组件。"""
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.login_page = login_page
        self.inbound_page = inbound_page
        self.inventory_page = inventory_page
        self.outbound_page = outbound_page
        self.api_client = api_client

    def login(self, base_url: str, login_path: str, username: str, password: str) -> None:
        """打开 WMS 登录页并完成用户认证。"""
        self.login_page.open_login(base_url, login_path)
        self.login_page.login(username, password)

    def create_inbound(self, base_url: str, receipt_no: str, sku_code: str) -> None:
        """导航到入库页面并创建指定 SKU 的入库单。"""
        self.inbound_page.open_inbound(base_url)
        self.inbound_page.create_receipt(receipt_no, sku_code)

    def query_inventory(self, base_url: str, sku_code: str) -> str:
        """打开库存页面、按 SKU 搜索并返回匹配行文本。"""
        self.inventory_page.open_inventory(base_url)
        self.inventory_page.search_inventory(sku_code)
        return self.inventory_page.inventory_row_text(sku_code)

    def create_outbound(self, base_url: str, outbound_no: str, sku_code: str) -> None:
        """导航到出库页面并创建指定 SKU 的出库单。"""
        self.outbound_page.open_outbound(base_url)
        self.outbound_page.create_outbound(outbound_no, sku_code)

    def fetch_inventory(self, sku_code: str) -> dict:
        """通过 API 接口查询指定 SKU 的实时库存数据。"""
        return self.api_client.query_inventory(sku_code)