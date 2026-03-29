"""中文说明：本模块封装弹窗类组件的定位与确认操作。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class DialogComponent(BaseComponent):
    def dialog(self):
        """中文说明：在 DialogComponent 中执行与 dialog 相关的操作。"""
        return self.smart_locator(
            "dialog",
            [
                LocatorCandidate("role-dialog", "[role='dialog']"),
                LocatorCandidate("modal-dialog", ".ant-modal,.el-dialog,.dialog"),
            ],
            "对话框定位",
        )

    def confirm(self) -> None:
        """中文说明：在 DialogComponent 中确认与 confirm 相关的操作。"""
        self.dialog().get_by_role("button", name="确定").click()