from __future__ import annotations

from api.base_client import ApiClient
from core.config.models import ApiSettings, SystemEndpoint


class WMSApiClient(ApiClient):
    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings) -> None:
        super().__init__(system_config, api_settings, api_settings.wms_endpoints)

    def get_inbound_detail(self, receipt_no: str) -> dict:
        return self.get("inbound_detail", receipt_no=receipt_no).json()

    def query_inventory(self, sku_code: str) -> dict:
        return self.get("inventory_query", params={"sku_code": sku_code}).json()

    def get_outbound_detail(self, outbound_no: str) -> dict:
        return self.get("outbound_detail", outbound_no=outbound_no).json()