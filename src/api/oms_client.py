from __future__ import annotations

from api.base_client import ApiClient
from core.config.models import ApiSettings, SystemEndpoint


class OMSApiClient(ApiClient):
    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings) -> None:
        super().__init__(system_config, api_settings, api_settings.oms_endpoints)

    def get_order_detail(self, order_no: str) -> dict:
        return self.get("order_detail", order_no=order_no).json()

    def search_order(self, keyword: str) -> dict:
        return self.get("order_search", params={"keyword": keyword}).json()