from __future__ import annotations

from typing import Any

import requests

from core.config.models import ApiSettings, SystemEndpoint


class ApiClient:
    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings, endpoint_map: dict[str, str]) -> None:
        self.system_config = system_config
        self.api_settings = api_settings
        self.endpoint_map = endpoint_map
        self.session = requests.Session()

    def build_url(self, endpoint_name: str, **path_params: Any) -> str:
        template = self.endpoint_map[endpoint_name]
        path = template.format(**path_params)
        return f"{self.system_config.base_url.rstrip('/')}{path}"

    def get(self, endpoint_name: str, *, params: dict[str, Any] | None = None, **path_params: Any) -> requests.Response:
        response = self.session.get(
            self.build_url(endpoint_name, **path_params),
            params=params,
            timeout=self.api_settings.timeout_seconds,
        )
        response.raise_for_status()
        return response