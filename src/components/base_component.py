from __future__ import annotations

from playwright.sync_api import Locator, Page

from ai.locator import SelfHealingLocator
from ai.models import LocatorCandidate


class BaseComponent:
    def __init__(self, page: Page, locator_strategy: SelfHealingLocator) -> None:
        self.page = page
        self.locator_strategy = locator_strategy

    def smart_locator(self, name: str, candidates: list[LocatorCandidate], context: str) -> Locator:
        resolution = self.locator_strategy.resolve(self.page, candidates, context)
        if not resolution.success:
            raise LookupError(f"组件定位失败: {name} | {context}")
        return self.page.locator(resolution.selector).first