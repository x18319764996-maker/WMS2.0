"""日期选择组件，封装日期输入框的填写操作。"""

from __future__ import annotations

from components.base_component import BaseComponent


class DatePickerComponent(BaseComponent):
    """日期选择器组件，通过填写日期字符串设置日期值。"""

    def set_date(self, input_selector: str, value: str) -> None:
        """向日期输入框填写日期字符串。"""
        self.page.locator(input_selector).fill(value)