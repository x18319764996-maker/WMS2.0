"""复杂控件基础抽象，统一接入自愈定位能力供子类控件复用。"""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from ai.locator import SelfHealingLocator
from ai.models import LocatorCandidate


class BaseComponent:
    """UI 组件基类，持有页面实例和自愈定位策略，子类继承后可直接使用 smart_locator。"""

    def __init__(self, page: Page, locator_strategy: SelfHealingLocator) -> None:
        """注入 Playwright Page 和自愈定位策略，供子类控件复用。"""
        self.page = page
        self.locator_strategy = locator_strategy

    def smart_locator(self, name: str, candidates: list[LocatorCandidate], context: str) -> Locator:
        """按候选列表调用自愈定位策略，返回第一个匹配的 Locator。"""
        resolution = self.locator_strategy.resolve(self.page, candidates, context)
        if not resolution.success:
            raise LookupError(f"组件定位失败: {name} | {context}")
        return self.page.locator(resolution.selector).first