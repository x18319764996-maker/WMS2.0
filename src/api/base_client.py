"""HTTP API 客户端基类，封装 URL 拼接、GET 请求和超时控制。"""

from __future__ import annotations

from typing import Any

import requests

from core.config.models import ApiSettings, SystemEndpoint


class ApiClient:
    """API 客户端基类，持有共享 HTTP Session 和接口路径模板映射。"""

    def __init__(self, system_config: SystemEndpoint, api_settings: ApiSettings, endpoint_map: dict[str, str]) -> None:
        """注入系统端点、API 全局配置和接口路径模板映射，并创建共享 HTTP Session。"""
        self.system_config = system_config
        self.api_settings = api_settings
        self.endpoint_map = endpoint_map
        self.session = requests.Session()

    def build_url(self, endpoint_name: str, **path_params: Any) -> str:
        """根据接口名称和路径参数拼接完整的请求 URL。"""
        template = self.endpoint_map[endpoint_name]
        path = template.format(**path_params)
        return f"{self.system_config.base_url.rstrip('/')}{path}"

    def get(self, endpoint_name: str, *, params: dict[str, Any] | None = None, **path_params: Any) -> requests.Response:
        """发送 GET 请求并返回 Response，自动应用全局超时。"""
        response = self.session.get(
            self.build_url(endpoint_name, **path_params),
            params=params,
            timeout=self.api_settings.timeout_seconds,
        )
        response.raise_for_status()
        return response