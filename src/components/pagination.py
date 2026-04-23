"""分页组件，封装页码按钮的跳页操作。"""

from __future__ import annotations

from components.base_component import BaseComponent


class PaginationComponent(BaseComponent):
    """分页控件组件，通过点击页码按钮实现分页跳转。"""

    def goto_page(self, page_no: int) -> None:
        """点击指定页码按钮跳转到目标分页。"""
        self.page.get_by_role("button", name=str(page_no)).click()