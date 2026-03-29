"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from components.window_manager import WindowManagerComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSCustomerProfilePage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(page, locator_strategy)
        self.window_manager = WindowManagerComponent(page, locator_strategy)

    def open_customer_profile(self, base_url: str) -> None:
        """中文说明：在 WMSCustomerProfilePage 中打开与 open_customer_profile 相关的操作。"""
        self.open(f"{base_url.rstrip('/')}/customer-profile")

    def jump_to_oms(self) -> str:
        """中文说明：在 WMSCustomerProfilePage 中执行与 jump_to_oms 相关的操作。"""
        popup = self.window_manager.open_popup("a:has-text('跳转OMS')")
        return popup.url