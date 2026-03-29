"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from ai.locator import SelfHealingLocator
from ai.models import LocatorCandidate
from core.waiting import WaitHelper


class BasePage:
    def __init__(self, page: Page, locator_strategy: SelfHealingLocator) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.page = page
        self.locator_strategy = locator_strategy
        self.wait = WaitHelper(page)

    def smart_locator(self, name: str, candidates: list[LocatorCandidate], context: str) -> Locator:
        """中文说明：在 BasePage 中执行与 smart_locator 相关的操作。"""
        resolution = self.locator_strategy.resolve(self.page, candidates, context)
        if not resolution.success:
            raise LookupError(f"页面定位失败: {name} | {context}")
        return self.page.locator(resolution.selector).first

    def open(self, url: str) -> None:
        """中文说明：在 BasePage 中打开与 open 相关的操作。"""
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def click(self, name: str, candidates: list[LocatorCandidate], context: str) -> None:
        """中文说明：在 BasePage 中点击与 click 相关的操作。"""
        self.smart_locator(name, candidates, context).click()

    def fill(self, name: str, value: str, candidates: list[LocatorCandidate], context: str) -> None:
        """中文说明：在 BasePage 中填写与 fill 相关的操作。"""
        locator = self.smart_locator(name, candidates, context)
        locator.fill(value)

    def expect_text(self, selector: str, expected_text: str) -> None:
        """中文说明：在 BasePage 中断言校验与 expect_text 相关的操作。"""
        expect(self.page.locator(selector)).to_contain_text(expected_text)