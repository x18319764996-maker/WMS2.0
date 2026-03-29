"""中文说明：本模块定义复杂控件的基础抽象，统一接入智能定位能力。"""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from ai.locator import SelfHealingLocator
from ai.models import LocatorCandidate


class BaseComponent:
    def __init__(self, page: Page, locator_strategy: SelfHealingLocator) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.page = page
        self.locator_strategy = locator_strategy

    def smart_locator(self, name: str, candidates: list[LocatorCandidate], context: str) -> Locator:
        """中文说明：在 BaseComponent 中执行与 smart_locator 相关的操作。"""
        resolution = self.locator_strategy.resolve(self.page, candidates, context)
        if not resolution.success:
            raise LookupError(f"组件定位失败: {name} | {context}")
        return self.page.locator(resolution.selector).first