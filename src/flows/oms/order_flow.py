"""OMS 订单业务流，串联登录→创建订单→搜索订单→API查询的完整链路。"""

from __future__ import annotations

from datetime import datetime

from api.oms_client import OMSApiClient
from flows.base_flow import BaseFlow
from pages.oms.login_page import OMSLoginPage
from pages.oms.order_page import OMSOrderPage


class OMSOrderFlow(BaseFlow):
    """OMS 订单核心业务流，组合登录页、订单页和 API 客户端，提供订单全生命周期操作。"""

    def __init__(self, login_page: OMSLoginPage, order_page: OMSOrderPage, api_client: OMSApiClient, assertion_assistant, failure_analysis_agent) -> None:
        """注入登录页、订单页、API 客户端和 AI 辅助组件。"""
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.login_page = login_page
        self.order_page = order_page
        self.api_client = api_client

    def login(self, base_url: str, login_path: str, username: str, password: str) -> None:
        """打开 OMS 登录页并完成用户认证。"""
        self.login_page.open_login(base_url, login_path)
        self.login_page.login(username, password)

    def create_order(self, base_url: str, customer_name: str, sku_code: str, quantity: int) -> str:
        """打开订单中心、填写订单信息并提交，返回生成的订单号。"""
        self.order_page.open_order_center(base_url)
        self.order_page.create_order(customer_name, sku_code, quantity)
        return f"SO-{datetime.now():%Y%m%d%H%M%S}"

    def search_order(self, base_url: str, keyword: str) -> None:
        """打开订单中心并按关键字搜索订单。"""
        self.order_page.open_order_center(base_url)
        self.order_page.search_order(keyword)

    def fetch_order_detail(self, order_no: str) -> dict:
        """通过 API 接口查询指定订单号的详情数据。"""
        return self.api_client.get_order_detail(order_no)