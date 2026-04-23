"""AI 断言助手。

当传统断言难以覆盖复杂页面状态（如表格数据语义校验）时，
可将页面摘要与期望值提交给大模型，获取辅助断言建议。
"""

from __future__ import annotations

from typing import Any

from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


class AssertionAssistant:
    """AI 断言助手，适用于传统 expect 难以覆盖的复杂语义校验场景。

    将页面摘要与期望条件提交给大模型，获取具体可执行的断言建议；
    AI 未启用时返回 enabled=False 的元数据，不影响正常用例执行。
    """

    def __init__(self, settings: AISettings, provider: OpenAICompatibleProvider | None = None) -> None:
        """注入 AI 配置与可选 Provider。"""
        self.settings = settings
        self.provider = provider

    def suggest(self, flow_name: str, expectations: dict[str, Any], page_summary: str) -> dict[str, Any]:
        """基于页面摘要与期望条件，请求模型给出断言建议。"""
        if self.settings.mode == "disabled" or not self.provider or not self.provider.is_available():
            return {
                "enabled": False,
                "reason": "AI 断言助手未启用",
                "flow_name": flow_name,
                "expectations": expectations,
            }
        response = self.provider.complete_json(
            "assertion_assistant",
            {
                "flow_name": flow_name,
                "expectations": expectations,
                "page_summary": page_summary[: self.settings.semantic_snapshot_limit],
            },
        )
        return response.content if response.success else {"enabled": False, "error": response.error}