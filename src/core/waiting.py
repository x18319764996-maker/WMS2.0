"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from playwright.sync_api import Locator, Page


class WaitHelper:
    def __init__(self, page: Page) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.page = page

    def for_visible(self, locator: Locator, timeout: int | None = None) -> Locator:
        """中文说明：在 WaitHelper 中执行与 for_visible 相关的操作。"""
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def for_network_idle(self, timeout: int | None = None) -> None:
        """中文说明：在 WaitHelper 中执行与 for_network_idle 相关的操作。"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)