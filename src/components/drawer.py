"""抽屉组件，封装侧边抽屉面板的智能定位操作。"""

from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class DrawerComponent(BaseComponent):
    """侧边抽屉组件，支持 Ant Design 等常见 UI 框架的抽屉定位。"""

    def drawer(self):
        """定位当前可见的侧边抽屉面板。"""
        return self.smart_locator(
            "drawer",
            [
                LocatorCandidate("drawer-common", ".ant-drawer,.drawer"),
                LocatorCandidate("drawer-role", "[role='complementary']"),
            ],
            "抽屉定位",
        )