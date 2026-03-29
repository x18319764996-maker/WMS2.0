"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from ai.models import AIResponse, DecisionTrace
from core.config.models import AISettings


class AIProvider(ABC):
    @abstractmethod
    def complete_json(self, task: str, payload: dict[str, Any]) -> AIResponse:
        """中文说明：在 AIProvider 中完成请求与 complete_json 相关的操作。"""
        raise NotImplementedError


class OpenAICompatibleProvider(AIProvider):
    def __init__(self, settings: AISettings) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.settings = settings
        self.session = requests.Session()

    def is_available(self) -> bool:
        """中文说明：在 OpenAICompatibleProvider 中判断与 is_available 相关的操作。"""
        return bool(self.settings.base_url and self.settings.api_key and self.settings.model)

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1), reraise=True)
    def _request(self, body: dict[str, Any]) -> requests.Response:
        """中文说明：在 OpenAICompatibleProvider 中执行与 _request 相关的操作。"""
        response = self.session.post(
            f"{self.settings.base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=self.settings.timeout_seconds,
        )
        response.raise_for_status()
        return response

    def complete_json(self, task: str, payload: dict[str, Any]) -> AIResponse:
        """中文说明：在 OpenAICompatibleProvider 中完成请求与 complete_json 相关的操作。"""
        if not self.is_available():
            return AIResponse(success=False, content={}, error="AI provider not configured")

        body = {
            "model": self.settings.model,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个 UI 自动化智能助手。请输出 JSON，并保持结果可解释。",
                },
                {
                    "role": "user",
                    "content": json.dumps({"task": task, "payload": payload}, ensure_ascii=False),
                },
            ],
        }
        try:
            response = self._request(body)
            raw = response.json()
            message = raw["choices"][0]["message"]["content"]
            content = json.loads(message)
            return AIResponse(success=True, content=content, raw_text=message)
        except Exception as exc:  # pragma: no cover - network behavior
            return AIResponse(success=False, content={}, error=str(exc))

    def append_audit_log(self, trace: DecisionTrace) -> None:
        """中文说明：在 OpenAICompatibleProvider 中追加与 append_audit_log 相关的操作。"""
        audit_path = Path(self.settings.audit_log_path)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(trace.to_dict(), ensure_ascii=False) + "\n")