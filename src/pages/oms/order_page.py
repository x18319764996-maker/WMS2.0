"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from components.dialog import DialogComponent
from components.table import TableComponent
from ai.models import LocatorCandidate
from pages.base_page import BasePage


class OMSOrderPage(BasePage):
    def __init__(self, page, locator_strategy) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(page, locator_strategy)
        self.dialog = DialogComponent(page, locator_strategy)
        self.table = TableComponent(page, locator_strategy)

    def open_order_center(self, base_url: str) -> None:
        """中文说明：在 OMSOrderPage 中打开与 open_order_center 相关的操作。"""
        self.open(f"{base_url.rstrip('/')}/orders")

    def create_order(self, customer_name: str, sku_code: str, quantity: int) -> None:
        """中文说明：在 OMSOrderPage 中创建与 create_order 相关的操作。"""
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
        """中文说明：在 OMSOrderPage 中查询与 search_order 相关的操作。"""
        self.fill("search_order", keyword, [LocatorCandidate("search-input", "input[placeholder*='订单']")], "OMS 订单搜索框")
        self.click("search_button", [LocatorCandidate("search-btn", "button:has-text('查询')")], "OMS 查询按钮")

    def current_status_text(self) -> str:
        """中文说明：在 OMSOrderPage 中执行与 current_status_text 相关的操作。"""
        return self.page.locator("table tr >> nth=1 td").first.text_content() or ""