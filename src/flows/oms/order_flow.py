from __future__ import annotations

from datetime import datetime

from api.oms_client import OMSApiClient
from flows.base_flow import BaseFlow
from pages.oms.login_page import OMSLoginPage
from pages.oms.order_page import OMSOrderPage


class OMSOrderFlow(BaseFlow):
    def __init__(self, login_page: OMSLoginPage, order_page: OMSOrderPage, api_client: OMSApiClient, assertion_assistant, failure_analysis_agent) -> None:
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.login_page = login_page
        self.order_page = order_page
        self.api_client = api_client

    def login(self, base_url: str, login_path: str, username: str, password: str) -> None:
        self.login_page.open_login(base_url, login_path)
        self.login_page.login(username, password)

    def create_order(self, base_url: str, customer_name: str, sku_code: str, quantity: int) -> str:
        self.order_page.open_order_center(base_url)
        self.order_page.create_order(customer_name, sku_code, quantity)
        return f"SO-{datetime.now():%Y%m%d%H%M%S}"

    def search_order(self, base_url: str, keyword: str) -> None:
        self.order_page.open_order_center(base_url)
        self.order_page.search_order(keyword)

    def fetch_order_detail(self, order_no: str) -> dict:
        return self.api_client.get_order_detail(order_no)