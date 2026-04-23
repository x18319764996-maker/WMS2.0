"""窗口管理组件，封装新窗口和弹出页的打开与等待逻辑。"""

from __future__ import annotations

from playwright.sync_api import Page

from components.base_component import BaseComponent


class WindowManagerComponent(BaseComponent):
    """窗口管理组件，点击触发元素后等待弹出窗口加载完成并返回新页面。"""

    def open_popup(self, trigger_selector: str) -> Page:
        """点击触发元素并等待弹出窗口加载完成，返回新窗口 Page。"""
        with self.page.expect_popup() as popup_info:
            self.page.locator(trigger_selector).click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        return popup