"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from pages.base_page import BasePage


class ExamplePage(BasePage):
    def open_page(self, base_url: str) -> None:
        """中文说明：在 ExamplePage 中打开与 open_page 相关的操作。"""
        self.open(f"{base_url.rstrip('/')}/example")

    def do_action(self) -> None:
        """中文说明：在 ExamplePage 中执行与 do_action 相关的操作。"""
        self.click(
            "example_action",
            [
                LocatorCandidate("primary", "button:has-text('操作')"),
                LocatorCandidate("fallback", "text=操作"),
            ],
            "示例页面操作按钮",
        )