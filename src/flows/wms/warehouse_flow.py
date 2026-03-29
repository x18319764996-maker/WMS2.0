from __future__ import annotations

from api.wms_client import WMSApiClient
from flows.base_flow import BaseFlow
from pages.wms.inbound_page import WMSInboundPage
from pages.wms.inventory_page import WMSInventoryPage
from pages.wms.login_page import WMSLoginPage
from pages.wms.outbound_page import WMSOutboundPage


class WMSWarehouseFlow(BaseFlow):
    def __init__(self, login_page: WMSLoginPage, inbound_page: WMSInboundPage, inventory_page: WMSInventoryPage, outbound_page: WMSOutboundPage, api_client: WMSApiClient, assertion_assistant, failure_analysis_agent) -> None:
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.login_page = login_page
        self.inbound_page = inbound_page
        self.inventory_page = inventory_page
        self.outbound_page = outbound_page
        self.api_client = api_client

    def login(self, base_url: str, login_path: str, username: str, password: str) -> None:
        self.login_page.open_login(base_url, login_path)
        self.login_page.login(username, password)

    def create_inbound(self, base_url: str, receipt_no: str, sku_code: str) -> None:
        self.inbound_page.open_inbound(base_url)
        self.inbound_page.create_receipt(receipt_no, sku_code)

    def query_inventory(self, base_url: str, sku_code: str) -> str:
        self.inventory_page.open_inventory(base_url)
        self.inventory_page.search_inventory(sku_code)
        return self.inventory_page.inventory_row_text(sku_code)

    def create_outbound(self, base_url: str, outbound_no: str, sku_code: str) -> None:
        self.outbound_page.open_outbound(base_url)
        self.outbound_page.create_outbound(outbound_no, sku_code)

    def fetch_inventory(self, sku_code: str) -> dict:
        return self.api_client.query_inventory(sku_code)