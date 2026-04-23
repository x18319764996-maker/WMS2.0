"""等待辅助类。

对 Playwright 原生等待做薄封装，统一默认超时与返回值，
减少页面与流代码中的重复样板。
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page


class WaitHelper:
    """等待辅助器，对 Playwright 原生等待做薄封装，统一超时和链式调用。"""

    def __init__(self, page: Page) -> None:
        """绑定目标页面。"""
        self.page = page

    def for_visible(self, locator: Locator, timeout: int | None = None) -> Locator:
        """等待元素可见并返回该元素，便于链式调用。"""
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def for_network_idle(self, timeout: int | None = None) -> None:
        """等待网络请求趋于空闲，适用于异步加载场景。"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)