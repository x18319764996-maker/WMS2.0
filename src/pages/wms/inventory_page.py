"""WMS 库存页面对象，封装库存搜索和行数据读取操作。"""

from __future__ import annotations

from components.table import TableComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class WMSInventoryPage(BasePage):
    """WMS 库存页，支持按 SKU 搜索库存和读取结果行文本。"""

    def __init__(self, page, locator_strategy) -> None:
        """注入页面、定位策略，并初始化表格组件用于行定位。"""
        super().__init__(page, locator_strategy)
        self.table = TableComponent(page, locator_strategy)

    def open_inventory(self, base_url: str) -> None:
        """导航到 WMS 库存页面。"""
        self.open(f"{base_url.rstrip('/')}/inventory")

    def search_inventory(self, sku_code: str) -> None:
        """填写 SKU 编码并点击查询按钮执行库存搜索。"""
        self.fill("inventory_search", sku_code, [LocatorCandidate("sku-search", "input[placeholder*='SKU']")], "库存查询 SKU")
        self.click("inventory_query", [LocatorCandidate("query-btn", "button:has-text('查询')")], "库存查询按钮")

    def inventory_row_text(self, sku_code: str) -> str:
        """读取表格中匹配 SKU 的行文本内容。"""
        return self.table.row_by_text("table", sku_code).text_content() or ""