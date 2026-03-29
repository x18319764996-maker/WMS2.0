"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from components.dialog import DialogComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSOutboundPage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(page, locator_strategy)
        self.dialog = DialogComponent(page, locator_strategy)

    def open_outbound(self, base_url: str) -> None:
        """中文说明：在 WMSOutboundPage 中打开与 open_outbound 相关的操作。"""
        self.open(f"{base_url.rstrip('/')}/outbound")

    def create_outbound(self, outbound_no: str, sku_code: str) -> None:
        """中文说明：在 WMSOutboundPage 中创建与 create_outbound 相关的操作。"""
        self.click("create_outbound", [LocatorCandidate("create-btn", "text=新建出库"), LocatorCandidate("create-alt", "button:has-text('出库新增')")], "WMS 出库新增")
        self.fill("outbound_no", outbound_no, [LocatorCandidate("outbound-input", "input[placeholder*='出库单']")], "出库单号")
        self.fill("sku_code", sku_code, [LocatorCandidate("sku-input", "input[placeholder*='SKU']")], "出库 SKU")
        self.dialog.confirm()