"""中文说明：本模块封装树结构控件的节点选择操作。"""

from __future__ import annotations

from components.base_component import BaseComponent


class TreeComponent(BaseComponent):
    def select_node(self, node_text: str) -> None:
        """中文说明：在 TreeComponent 中选择与 select_node 相关的操作。"""
        self.page.get_by_text(node_text, exact=True).click()