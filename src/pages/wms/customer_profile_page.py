from __future__ import annotations

from components.window_manager import WindowManagerComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSCustomerProfilePage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        super().__init__(page, locator_strategy)
        self.window_manager = WindowManagerComponent(page, locator_strategy)

    def open_customer_profile(self, base_url: str) -> None:
        self.open(f"{base_url.rstrip('/')}/customer-profile")

    def jump_to_oms(self) -> str:
        popup = self.window_manager.open_popup("a:has-text('跳转OMS')")
        return popup.url