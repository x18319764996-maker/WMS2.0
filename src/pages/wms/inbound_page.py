"""WMS 入库页面对象，封装入库单创建流程。"""

from __future__ import annotations

from components.dialog import DialogComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSInboundPage(BasePage):
    """WMS 入库页，支持导航到入库页面和创建入库单。"""

    def __init__(self, page, locator_strategy) -> None:
        """注入页面、定位策略，并初始化弹窗组件用于入库确认。"""
        super().__init__(page, locator_strategy)
        self.dialog = DialogComponent(page, locator_strategy)

    def open_inbound(self, base_url: str) -> None:
        """导航到 WMS 入库页面。"""
        self.open(f"{base_url.rstrip('/')}/inbound")

    def create_receipt(self, receipt_no: str, sku_code: str) -> None:
        """填写入库单号和 SKU 编码，并通过弹窗确认提交入库。"""
        self.click("create_receipt", [LocatorCandidate("create-btn", "text=新建入库"), LocatorCandidate("create-alt", "button:has-text('入库新增')")], "WMS 入库新增")
        self.fill("receipt_no", receipt_no, [LocatorCandidate("receipt-input", "input[placeholder*='入库单']")], "入库单号")
        self.fill("sku_code", sku_code, [LocatorCandidate("sku-input", "input[placeholder*='SKU']")], "入库 SKU")
        self.dialog.confirm()