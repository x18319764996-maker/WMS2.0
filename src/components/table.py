"""中文说明：本模块封装表格组件的行定位和行内操作。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class TableComponent(BaseComponent):
    def row_by_text(self, table_selector: str, text: str):
        """中文说明：在 TableComponent 中执行与 row_by_text 相关的操作。"""
        return self.page.locator(f"{table_selector} tr", has_text=text).first

    def click_action(self, table_selector: str, row_text: str, action_text: str) -> None:
        """中文说明：在 TableComponent 中点击与 click_action 相关的操作。"""
        row = self.row_by_text(table_selector, row_text)
        row.get_by_role("button", name=action_text).click()

    def locate_table(self, context: str):
        """中文说明：在 TableComponent 中执行与 locate_table 相关的操作。"""
        return self.smart_locator(
            "table",
            [
                LocatorCandidate("table-role", "[role='table']"),
                LocatorCandidate("table-native", "table"),
            ],
            context,
        )