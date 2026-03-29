"""中文说明：本模块封装分页控件的跳页操作。"""

from __future__ import annotations

from components.base_component import BaseComponent


class PaginationComponent(BaseComponent):
    def goto_page(self, page_no: int) -> None:
        """中文说明：在 PaginationComponent 中执行与 goto_page 相关的操作。"""
        self.page.get_by_role("button", name=str(page_no)).click()