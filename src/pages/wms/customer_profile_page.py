"""WMS 客户档案页面对象，封装客户档案查看和跨系统跳转操作。"""

from __future__ import annotations

from components.window_manager import WindowManagerComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSCustomerProfilePage(BasePage):
    """WMS 客户档案页，支持打开档案和跳转到 OMS 新窗口。"""

    def __init__(self, page, locator_strategy) -> None:
        """注入页面、定位策略，并初始化窗口管理组件用于跨系统跳转。"""
        super().__init__(page, locator_strategy)
        self.window_manager = WindowManagerComponent(page, locator_strategy)

    def open_customer_profile(self, base_url: str) -> None:
        """导航到 WMS 客户档案页面。"""
        self.open(f"{base_url.rstrip('/')}/customer-profile")

    def jump_to_oms(self) -> str:
        """点击"跳转OMS"链接，等待新窗口加载并返回其 URL。"""
        popup = self.window_manager.open_popup("a:has-text('跳转OMS')")
        return popup.url