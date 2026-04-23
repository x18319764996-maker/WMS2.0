"""虚拟滚动列表组件，封装在虚拟滚动容器中逐页滚动查找目标元素的逻辑。"""

from __future__ import annotations

from components.base_component import BaseComponent


class VirtualListComponent(BaseComponent):
    """虚拟滚动列表组件，逐页滚动直到目标文本可见或达到上限。"""

    def scroll_until_visible(self, container_selector: str, item_text: str, max_scrolls: int = 10) -> None:
        """在虚拟滚动容器中逐页滚动直到目标文本可见，超限后抛出 LookupError。"""
        container = self.page.locator(container_selector)
        for _ in range(max_scrolls):
            if self.page.get_by_text(item_text).count() > 0:
                return
            container.evaluate("element => element.scrollBy(0, element.clientHeight)")
        raise LookupError(f"未在虚拟列表中找到: {item_text}")