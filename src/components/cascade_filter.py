"""联动筛选组件，封装多级联动筛选器的展开与选择操作。"""

from __future__ import annotations

from components.base_component import BaseComponent


class CascadeFilterComponent(BaseComponent):
    """联动筛选器组件，依次展开下拉并选择选项实现多级筛选。"""

    def apply_filters(self, filters: list[tuple[str, str]]) -> None:
        """依次展开筛选器并选择选项，实现多级联动筛选。"""
        for trigger_selector, option_text in filters:
            self.page.locator(trigger_selector).click()
            self.page.get_by_text(option_text, exact=True).click()