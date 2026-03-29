from __future__ import annotations

from components.dialog import DialogComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSInboundPage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        super().__init__(page, locator_strategy)
        self.dialog = DialogComponent(page, locator_strategy)

    def open_inbound(self, base_url: str) -> None:
        self.open(f"{base_url.rstrip('/')}/inbound")

    def create_receipt(self, receipt_no: str, sku_code: str) -> None:
        self.click("create_receipt", [LocatorCandidate("create-btn", "text=新建入库"), LocatorCandidate("create-alt", "button:has-text('入库新增')")], "WMS 入库新增")
        self.fill("receipt_no", receipt_no, [LocatorCandidate("receipt-input", "input[placeholder*='入库单']")], "入库单号")
        self.fill("sku_code", sku_code, [LocatorCandidate("sku-input", "input[placeholder*='SKU']")], "入库 SKU")
        self.dialog.confirm()