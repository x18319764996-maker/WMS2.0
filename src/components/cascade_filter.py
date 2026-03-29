"""中文说明：本模块封装联动筛选控件的常用操作。"""

from __future__ import annotations

from components.base_component import BaseComponent


class CascadeFilterComponent(BaseComponent):
    def apply_filters(self, filters: list[tuple[str, str]]) -> None:
        """中文说明：在 CascadeFilterComponent 中应用与 apply_filters 相关的操作。"""
        for trigger_selector, option_text in filters:
            self.page.locator(trigger_selector).click()
            self.page.get_by_text(option_text, exact=True).click()