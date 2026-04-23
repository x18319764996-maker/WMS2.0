"""页面对象脚手架模板，新建页面对象时可复制此文件并按需修改。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from pages.base_page import BasePage


class ExamplePage(BasePage):
    """示例页面对象，演示导航和操作按钮的基本结构。"""

    def open_page(self, base_url: str) -> None:
        """导航到示例页面。"""
        self.open(f"{base_url.rstrip('/')}/example")

    def do_action(self) -> None:
        """点击示例操作按钮。"""
        self.click(
            "example_action",
            [
                LocatorCandidate("primary", "button:has-text('操作')"),
                LocatorCandidate("fallback", "text=操作"),
            ],
            "示例页面操作按钮",
        )