from __future__ import annotations

from components.base_component import BaseComponent


class DatePickerComponent(BaseComponent):
    def set_date(self, input_selector: str, value: str) -> None:
        self.page.locator(input_selector).fill(value)