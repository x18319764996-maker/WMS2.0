from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class DialogComponent(BaseComponent):
    def dialog(self):
        return self.smart_locator(
            "dialog",
            [
                LocatorCandidate("role-dialog", "[role='dialog']"),
                LocatorCandidate("modal-dialog", ".ant-modal,.el-dialog,.dialog"),
            ],
            "对话框定位",
        )

    def confirm(self) -> None:
        self.dialog().get_by_role("button", name="确定").click()