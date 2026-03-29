from __future__ import annotations

from ai.models import LocatorCandidate
from components.base_component import BaseComponent


class DrawerComponent(BaseComponent):
    def drawer(self):
        return self.smart_locator(
            "drawer",
            [
                LocatorCandidate("drawer-common", ".ant-drawer,.drawer"),
                LocatorCandidate("drawer-role", "[role='complementary']"),
            ],
            "抽屉定位",
        )