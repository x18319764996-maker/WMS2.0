from __future__ import annotations

from playwright.sync_api import Locator, Page


class WaitHelper:
    def __init__(self, page: Page) -> None:
        self.page = page

    def for_visible(self, locator: Locator, timeout: int | None = None) -> Locator:
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def for_network_idle(self, timeout: int | None = None) -> None:
        self.page.wait_for_load_state("networkidle", timeout=timeout)