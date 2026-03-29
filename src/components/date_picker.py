"""中文说明：本模块封装日期控件的基础交互。"""

from __future__ import annotations

from components.base_component import BaseComponent


class DatePickerComponent(BaseComponent):
    def set_date(self, input_selector: str, value: str) -> None:
        """中文说明：在 DatePickerComponent 中设置与 set_date 相关的操作。"""
        self.page.locator(input_selector).fill(value)