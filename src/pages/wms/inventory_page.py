from __future__ import annotations

from components.table import TableComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSInventoryPage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        super().__init__(page, locator_strategy)
        self.table = TableComponent(page, locator_strategy)

    def open_inventory(self, base_url: str) -> None:
        self.open(f"{base_url.rstrip('/')}/inventory")

    def search_inventory(self, sku_code: str) -> None:
        self.fill("inventory_search", sku_code, [LocatorCandidate("sku-search", "input[placeholder*='SKU']")], "库存查询 SKU")
        self.click("inventory_query", [LocatorCandidate("query-btn", "button:has-text('查询')")], "库存查询按钮")

    def inventory_row_text(self, sku_code: str) -> str:
        return self.table.row_by_text("table", sku_code).text_content() or ""