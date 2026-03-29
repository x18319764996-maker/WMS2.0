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
        raise NotImplementedError


class OpenAICompatibleProvider(AIProvider):
    def __init__(self, settings: AISettings) -> None:
        self.settings = settings
        self.session = requests.Session()

    def is_available(self) -> bool:
        return bool(self.settings.base_url and self.settings.api_key and self.settings.model)

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1), reraise=True)
    def _request(self, body: dict[str, Any]) -> requests.Response:
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
        audit_path = Path(self.settings.audit_log_path)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(trace.to_dict(), ensure_ascii=False) + "\n")