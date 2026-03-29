"""中文说明：本模块封装抽屉类组件的通用操作。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class DrawerComponent(BaseComponent):
    def drawer(self):
        """中文说明：在 DrawerComponent 中执行与 drawer 相关的操作。"""
        return self.smart_locator(
            "drawer",
            [
                LocatorCandidate("drawer-common", ".ant-drawer,.drawer"),
                LocatorCandidate("drawer-role", "[role='complementary']"),
            ],
            "抽屉定位",
        )