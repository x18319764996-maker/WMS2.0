from __future__ import annotations

from components.dialog import DialogComponent
from components.table import TableComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class OMSOrderPage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        super().__init__(page, locator_strategy)
        self.dialog = DialogComponent(page, locator_strategy)
        self.table = TableComponent(page, locator_strategy)

    def open_order_center(self, base_url: str) -> None:
        self.open(f"{base_url.rstrip('/')}/orders")

    def create_order(self, customer_name: str, sku_code: str, quantity: int) -> None:
        self.click(
            "create_order",
            [LocatorCandidate("create-button", "text=创建订单"), LocatorCandidate("new-button", "button:has-text('新建')")],
            "OMS 创建订单入口",
        )
        self.fill("customer_name", customer_name, [LocatorCandidate("customer-input", "input[placeholder*='客户']")], "客户名称")
        self.fill("sku_code", sku_code, [LocatorCandidate("sku-input", "input[placeholder*='SKU']")], "SKU 编码")
        self.fill("quantity", str(quantity), [LocatorCandidate("quantity-input", "input[placeholder*='数量']")], "数量")
        self.dialog.confirm()

    def search_order(self, keyword: str) -> None:
        self.fill("search_order", keyword, [LocatorCandidate("search-input", "input[placeholder*='订单']")], "OMS 订单搜索框")
        self.click("search_button", [LocatorCandidate("search-btn", "button:has-text('查询')")], "OMS 查询按钮")

    def current_status_text(self) -> str:
        return self.page.locator("table tr >> nth=1 td").first.text_content() or ""