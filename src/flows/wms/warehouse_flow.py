"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from api.wms_client import WMSApiClient
from flows.base_flow import BaseFlow
from pages.wms.inbound_page import WMSInboundPage
from pages.wms.inventory_page import WMSInventoryPage
from pages.wms.login_page import WMSLoginPage
from pages.wms.outbound_page import WMSOutboundPage


class WMSWarehouseFlow(BaseFlow):
    def __init__(self, login_page: WMSLoginPage, inbound_page: WMSInboundPage, inventory_page: WMSInventoryPage, outbound_page: WMSOutboundPage, api_client: WMSApiClient, assertion_assistant, failure_analysis_agent) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.login_page = login_page
        self.inbound_page = inbound_page
        self.inventory_page = inventory_page
        self.outbound_page = outbound_page
        self.api_client = api_client

    def login(self, base_url: str, login_path: str, username: str, password: str) -> None:
        """中文说明：在 WMSWarehouseFlow 中执行登录与 login 相关的操作。"""
        self.login_page.open_login(base_url, login_path)
        self.login_page.login(username, password)

    def create_inbound(self, base_url: str, receipt_no: str, sku_code: str) -> None:
        """中文说明：在 WMSWarehouseFlow 中创建与 create_inbound 相关的操作。"""
        self.inbound_page.open_inbound(base_url)
        self.inbound_page.create_receipt(receipt_no, sku_code)

    def query_inventory(self, base_url: str, sku_code: str) -> str:
        """中文说明：在 WMSWarehouseFlow 中查询与 query_inventory 相关的操作。"""
        self.inventory_page.open_inventory(base_url)
        self.inventory_page.search_inventory(sku_code)
        return self.inventory_page.inventory_row_text(sku_code)

    def create_outbound(self, base_url: str, outbound_no: str, sku_code: str) -> None:
        """中文说明：在 WMSWarehouseFlow 中创建与 create_outbound 相关的操作。"""
        self.outbound_page.open_outbound(base_url)
        self.outbound_page.create_outbound(outbound_no, sku_code)

    def fetch_inventory(self, sku_code: str) -> dict:
        """中文说明：在 WMSWarehouseFlow 中获取与 fetch_inventory 相关的操作。"""
        return self.api_client.query_inventory(sku_code)