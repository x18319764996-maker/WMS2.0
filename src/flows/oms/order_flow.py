"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from datetime import datetime

from api.oms_client import OMSApiClient
from flows.base_flow import BaseFlow
from pages.oms.login_page import OMSLoginPage
from pages.oms.order_page import OMSOrderPage


class OMSOrderFlow(BaseFlow):
    def __init__(self, login_page: OMSLoginPage, order_page: OMSOrderPage, api_client: OMSApiClient, assertion_assistant, failure_analysis_agent) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.login_page = login_page
        self.order_page = order_page
        self.api_client = api_client

    def login(self, base_url: str, login_path: str, username: str, password: str) -> None:
        """中文说明：在 OMSOrderFlow 中执行登录与 login 相关的操作。"""
        self.login_page.open_login(base_url, login_path)
        self.login_page.login(username, password)

    def create_order(self, base_url: str, customer_name: str, sku_code: str, quantity: int) -> str:
        """中文说明：在 OMSOrderFlow 中创建与 create_order 相关的操作。"""
        self.order_page.open_order_center(base_url)
        self.order_page.create_order(customer_name, sku_code, quantity)
        return f"SO-{datetime.now():%Y%m%d%H%M%S}"

    def search_order(self, base_url: str, keyword: str) -> None:
        """中文说明：在 OMSOrderFlow 中查询与 search_order 相关的操作。"""
        self.order_page.open_order_center(base_url)
        self.order_page.search_order(keyword)

    def fetch_order_detail(self, order_no: str) -> dict:
        """中文说明：在 OMSOrderFlow 中获取与 fetch_order_detail 相关的操作。"""
        return self.api_client.get_order_detail(order_no)