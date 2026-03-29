"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from components.table import TableComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSInventoryPage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(page, locator_strategy)
        self.table = TableComponent(page, locator_strategy)

    def open_inventory(self, base_url: str) -> None:
        """中文说明：在 WMSInventoryPage 中打开与 open_inventory 相关的操作。"""
        self.open(f"{base_url.rstrip('/')}/inventory")

    def search_inventory(self, sku_code: str) -> None:
        """中文说明：在 WMSInventoryPage 中查询与 search_inventory 相关的操作。"""
        self.fill("inventory_search", sku_code, [LocatorCandidate("sku-search", "input[placeholder*='SKU']")], "库存查询 SKU")
        self.click("inventory_query", [LocatorCandidate("query-btn", "button:has-text('查询')")], "库存查询按钮")

    def inventory_row_text(self, sku_code: str) -> str:
        """中文说明：在 WMSInventoryPage 中执行与 inventory_row_text 相关的操作。"""
        return self.table.row_by_text("table", sku_code).text_content() or ""