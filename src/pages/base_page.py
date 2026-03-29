from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from ai.locator import SelfHealingLocator
from ai.models import LocatorCandidate
from core.waiting import WaitHelper


class BasePage:
    def __init__(self, page: Page, locator_strategy: SelfHealingLocator) -> None:
        self.page = page
        self.locator_strategy = locator_strategy
        self.wait = WaitHelper(page)

    def smart_locator(self, name: str, candidates: list[LocatorCandidate], context: str) -> Locator:
        resolution = self.locator_strategy.resolve(self.page, candidates, context)
        if not resolution.success:
            raise LookupError(f"页面定位失败: {name} | {context}")
        return self.page.locator(resolution.selector).first

    def open(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def click(self, name: str, candidates: list[LocatorCandidate], context: str) -> None:
        self.smart_locator(name, candidates, context).click()

    def fill(self, name: str, value: str, candidates: list[LocatorCandidate], context: str) -> None:
        locator = self.smart_locator(name, candidates, context)
        locator.fill(value)

    def expect_text(self, selector: str, expected_text: str) -> None:
        expect(self.page.locator(selector)).to_contain_text(expected_text)