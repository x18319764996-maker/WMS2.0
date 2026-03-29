from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class TableComponent(BaseComponent):
    def row_by_text(self, table_selector: str, text: str):
        return self.page.locator(f"{table_selector} tr", has_text=text).first

    def click_action(self, table_selector: str, row_text: str, action_text: str) -> None:
        row = self.row_by_text(table_selector, row_text)
        row.get_by_role("button", name=action_text).click()

    def locate_table(self, context: str):
        return self.smart_locator(
            "table",
            [
                LocatorCandidate("table-role", "[role='table']"),
                LocatorCandidate("table-native", "table"),
            ],
            context,
        )