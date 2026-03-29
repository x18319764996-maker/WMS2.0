from __future__ import annotations

from components.base_component import BaseComponent


class PaginationComponent(BaseComponent):
    def goto_page(self, page_no: int) -> None:
        self.page.get_by_role("button", name=str(page_no)).click()