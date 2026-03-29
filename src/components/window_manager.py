from __future__ import annotations

from playwright.sync_api import Page

from components.base_component import BaseComponent


class WindowManagerComponent(BaseComponent):
    def open_popup(self, trigger_selector: str) -> Page:
        with self.page.expect_popup() as popup_info:
            self.page.locator(trigger_selector).click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        return popup