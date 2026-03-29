from __future__ import annotations

from ai.models import LocatorCandidate
from pages.base_page import BasePage


class ExamplePage(BasePage):
    def open_page(self, base_url: str) -> None:
        self.open(f"{base_url.rstrip('/')}/example")

    def do_action(self) -> None:
        self.click(
            "example_action",
            [
                LocatorCandidate("primary", "button:has-text('操作')"),
                LocatorCandidate("fallback", "text=操作"),
            ],
            "示例页面操作按钮",
        )