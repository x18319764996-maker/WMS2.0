"""中文说明：本模块封装新窗口和弹出页的处理逻辑。"""

from __future__ import annotations

from playwright.sync_api import Page

from components.base_component import BaseComponent


class WindowManagerComponent(BaseComponent):
    def open_popup(self, trigger_selector: str) -> Page:
        """中文说明：在 WindowManagerComponent 中打开与 open_popup 相关的操作。"""
        with self.page.expect_popup() as popup_info:
            self.page.locator(trigger_selector).click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        return popup