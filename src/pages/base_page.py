"""所有页面对象的基类。

封装了基于自愈定位器的常用 UI 操作（点击、填写、断言），
子类只需声明元素定位候选（LocatorCandidate）即可复用智能解析逻辑。
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from ai.locator import SelfHealingLocator
from ai.models import LocatorCandidate
from core.waiting import WaitHelper


class BasePage:
    """页面对象基类，封装自愈定位、导航、点击、填写和断言等通用 UI 操作。"""

    def __init__(self, page: Page, locator_strategy: SelfHealingLocator) -> None:
        """注入 Playwright Page 与自愈定位策略。"""
        self.page = page
        self.locator_strategy = locator_strategy
        self.wait = WaitHelper(page)

    def smart_locator(self, name: str, candidates: list[LocatorCandidate], context: str) -> Locator:
        """按候选列表依次尝试定位；全部失败时视 AI 配置决定是否调用自愈服务。"""
        resolution = self.locator_strategy.resolve(self.page, candidates, context)
        if not resolution.success:
            raise LookupError(f"页面定位失败: {name} | {context}")
        return self.page.locator(resolution.selector).first

    def open(self, url: str) -> None:
        """导航到指定 URL 并等待 DOMContentLoaded。"""
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def click(self, name: str, candidates: list[LocatorCandidate], context: str) -> None:
        """智能定位并点击元素。"""
        self.smart_locator(name, candidates, context).click()

    def fill(self, name: str, value: str, candidates: list[LocatorCandidate], context: str) -> None:
        """智能定位并填写输入框。"""
        locator = self.smart_locator(name, candidates, context)
        locator.fill(value)

    def expect_text(self, selector: str, expected_text: str) -> None:
        """使用 Playwright expect 断言元素包含指定文本。"""
        expect(self.page.locator(selector)).to_contain_text(expected_text)