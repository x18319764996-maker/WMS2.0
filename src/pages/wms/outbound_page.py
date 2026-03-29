from __future__ import annotations

from components.dialog import DialogComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSOutboundPage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        super().__init__(page, locator_strategy)
        self.dialog = DialogComponent(page, locator_strategy)

    def open_outbound(self, base_url: str) -> None:
        self.open(f"{base_url.rstrip('/')}/outbound")

    def create_outbound(self, outbound_no: str, sku_code: str) -> None:
        self.click("create_outbound", [LocatorCandidate("create-btn", "text=新建出库"), LocatorCandidate("create-alt", "button:has-text('出库新增')")], "WMS 出库新增")
        self.fill("outbound_no", outbound_no, [LocatorCandidate("outbound-input", "input[placeholder*='出库单']")], "出库单号")
        self.fill("sku_code", sku_code, [LocatorCandidate("sku-input", "input[placeholder*='SKU']")], "出库 SKU")
        self.dialog.confirm()