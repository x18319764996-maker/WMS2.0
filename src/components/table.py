"""表格组件，封装行定位、行内按钮点击和表格根元素智能定位。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class TableComponent(BaseComponent):
    """表格交互组件，支持按文本定位行、点击行内操作按钮和智能定位表格根元素。"""

    def row_by_text(self, table_selector: str, text: str):
        """在表格中按文本内容定位目标行。"""
        return self.page.locator(f"{table_selector} tr", has_text=text).first

    def click_action(self, table_selector: str, row_text: str, action_text: str) -> None:
        """在指定行内点击操作按钮（如编辑、删除）。"""
        row = self.row_by_text(table_selector, row_text)
        row.get_by_role("button", name=action_text).click()

    def locate_table(self, context: str):
        """通过自愈定位策略定位页面上的表格根元素。"""
        return self.smart_locator(
            "table",
            [
                LocatorCandidate("table-role", "[role='table']"),
                LocatorCandidate("table-native", "table"),
            ],
            context,
        )