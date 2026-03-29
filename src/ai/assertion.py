from __future__ import annotations

from typing import Any

from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


class AssertionAssistant:
    def __init__(self, settings: AISettings, provider: OpenAICompatibleProvider | None = None) -> None:
        self.settings = settings
        self.provider = provider

    def suggest(self, flow_name: str, expectations: dict[str, Any], page_summary: str) -> dict[str, Any]:
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