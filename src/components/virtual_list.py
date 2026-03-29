"""中文说明：本模块封装虚拟滚动列表的滚动查找逻辑。"""

from __future__ import annotations

from components.base_component import BaseComponent


class VirtualListComponent(BaseComponent):
    def scroll_until_visible(self, container_selector: str, item_text: str, max_scrolls: int = 10) -> None:
        """中文说明：在 VirtualListComponent 中滚动查找与 scroll_until_visible 相关的操作。"""
        container = self.page.locator(container_selector)
        for _ in range(max_scrolls):
            if self.page.get_by_text(item_text).count() > 0:
                return
            container.evaluate("element => element.scrollBy(0, element.clientHeight)")
        raise LookupError(f"未在虚拟列表中找到: {item_text}")