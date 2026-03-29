from __future__ import annotations

from domains.cross_system.context import CrossSystemOrderContext
from flows.base_flow import BaseFlow
from flows.oms.order_flow import OMSOrderFlow
from flows.wms.warehouse_flow import WMSWarehouseFlow
from pages.wms.customer_profile_page import WMSCustomerProfilePage


class CrossSystemOrderFulfillmentFlow(BaseFlow):
    def __init__(self, oms_flow: OMSOrderFlow, wms_flow: WMSWarehouseFlow, customer_profile_page: WMSCustomerProfilePage, assertion_assistant, failure_analysis_agent) -> None:
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.oms_flow = oms_flow
        self.wms_flow = wms_flow
        self.customer_profile_page = customer_profile_page

    def run_order_to_warehouse(self, oms_base_url: str, wms_base_url: str, oms_login_path: str, wms_login_path: str, oms_credentials: tuple[str, str], wms_credentials: tuple[str, str], customer_name: str, sku_code: str, quantity: int) -> CrossSystemOrderContext:
        context = CrossSystemOrderContext(sku_code=sku_code)
        self.oms_flow.login(oms_base_url, oms_login_path, *oms_credentials)
        context.order_no = self.oms_flow.create_order(oms_base_url, customer_name, sku_code, quantity)
        self.oms_flow.search_order(oms_base_url, context.order_no)

        self.wms_flow.login(wms_base_url, wms_login_path, *wms_credentials)
        context.receipt_no = f"IN-{context.order_no}"
        self.wms_flow.create_inbound(wms_base_url, context.receipt_no, sku_code)
        context.outbound_no = f"OUT-{context.order_no}"
        self.wms_flow.create_outbound(wms_base_url, context.outbound_no, sku_code)
        return context

    def jump_from_wms_to_oms(self, wms_base_url: str) -> str:
        self.customer_profile_page.open_customer_profile(wms_base_url)
        return self.customer_profile_page.jump_to_oms()