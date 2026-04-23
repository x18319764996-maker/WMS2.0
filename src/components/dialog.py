"""弹窗组件，封装弹窗定位与确认按钮点击操作。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class DialogComponent(BaseComponent):
    """弹窗交互组件，支持 Ant Design / Element UI 等常见弹窗框架。"""

    def dialog(self):
        """定位当前可见的弹窗元素。"""
        return self.smart_locator(
            "dialog",
            [
                LocatorCandidate("role-dialog", "[role='dialog']"),
                LocatorCandidate("modal-dialog", ".ant-modal,.el-dialog,.dialog"),
            ],
            "对话框定位",
        )

    def confirm(self) -> None:
        """点击弹窗中的"确定"按钮完成确认操作。"""
        self.dialog().get_by_role("button", name="确定").click()