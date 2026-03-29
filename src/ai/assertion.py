"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from typing import Any

from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


class AssertionAssistant:
    def __init__(self, settings: AISettings, provider: OpenAICompatibleProvider | None = None) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.settings = settings
        self.provider = provider

    def suggest(self, flow_name: str, expectations: dict[str, Any], page_summary: str) -> dict[str, Any]:
        """中文说明：在 AssertionAssistant 中生成建议与 suggest 相关的操作。"""
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