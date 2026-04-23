"""树结构组件，封装树节点的精确选择操作。"""

from __future__ import annotations

from components.base_component import BaseComponent


class TreeComponent(BaseComponent):
    """树控件组件，按节点文本精确匹配并点击目标节点。"""

    def select_node(self, node_text: str) -> None:
        """按节点文本精确匹配并点击树结构中的目标节点。"""
        self.page.get_by_text(node_text, exact=True).click()