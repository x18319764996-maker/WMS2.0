from __future__ import annotations

from components.base_component import BaseComponent


class TreeComponent(BaseComponent):
    def select_node(self, node_text: str) -> None:
        self.page.get_by_text(node_text, exact=True).click()