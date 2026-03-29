"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from typing import Any

import requests

from core.config.models import ApiSettings, SystemEndpoint


class ApiClient:
    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings, endpoint_map: dict[str, str]) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.system_config = system_config
        self.api_settings = api_settings
        self.endpoint_map = endpoint_map
        self.session = requests.Session()

    def build_url(self, endpoint_name: str, **path_params: Any) -> str:
        """中文说明：在 ApiClient 中构建与 build_url 相关的操作。"""
        template = self.endpoint_map[endpoint_name]
        path = template.format(**path_params)
        return f"{self.system_config.base_url.rstrip('/')}{path}"

    def get(self, endpoint_name: str, *, params: dict[str, Any] | None = None, **path_params: Any) -> requests.Response:
        """中文说明：在 ApiClient 中获取与 get 相关的操作。"""
        response = self.session.get(
            self.build_url(endpoint_name, **path_params),
            params=params,
            timeout=self.api_settings.timeout_seconds,
        )
        response.raise_for_status()
        return response