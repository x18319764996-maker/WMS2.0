"""OpenAI 兼容格式的 AI Provider 实现。

支持对话补全、JSON 结构化输出、自动重试与审计日志追加，
可通过环境变量灵活切换不同模型端点（如 OpenAI、Azure、本地 vLLM）。
"""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from ai.models import AIResponse, DecisionTrace
from core.config.models import AISettings


class AIProvider(ABC):
    """AI 提供者抽象接口，定义 complete_json 契约，子类需实现具体的模型对接。"""

    @abstractmethod
    def complete_json(self, task: str, payload: dict[str, Any]) -> AIResponse:
        """向模型发送任务与上下文，返回结构化 JSON 响应。"""
        raise NotImplementedError


class OpenAICompatibleProvider(AIProvider):
    """基于 OpenAI 兼容格式的 AI 提供者实现。

    支持 OpenAI、Azure、vLLM、GLM 等兼容端点；内置 tenacity 指数退避重试、
    任务提示词映射（TASK_PROMPTS）和 JSONL 审计日志追加机制。
    """

    TASK_PROMPTS: dict[str, str] = {
        "heal_locator": (
            "你是一个Web UI自动化测试的定位器自愈专家。\n"
            "你将收到一组失败的CSS候选定位器、页面DOM片段和上下文描述。\n"
            "请分析DOM结构，推断目标元素最可靠的CSS选择器。\n"
            "优先使用id、data-testid、aria属性，避免脆弱的层级路径。\n"
            '严格返回JSON格式: {"selector": "<有效的CSS选择器>"}'
        ),
        "assertion_assistant": (
            "你是一个UI自动化测试的智能断言助手。\n"
            "你将收到业务流名称、期望条件和页面HTML摘要。\n"
            "请根据页面实际内容，给出具体可执行的断言建议。\n"
            '返回JSON格式: {"assertions": [{"check": "描述", "selector": "...", "expected": "..."}], '
            '"confidence": 0.0-1.0, "reasoning": "..."}'
        ),
        "failure_analysis": (
            "你是一个UI自动化测试失败诊断专家。\n"
            "你将收到失败步骤名、异常信息、额外上下文和页面快照。\n"
            "请分析根因并给出具体可操作的修复建议。\n"
            "classification必须为以下之一: timeout, ui_failure, network_error, data_mismatch, unknown\n"
            '返回JSON格式: {"probable_cause": "...", "suggestion": "...", "classification": "..."}'
        ),
    }

    DEFAULT_PROMPT = "你是一个 UI 自动化智能助手。请输出 JSON，并保持结果可解释。"

    def __init__(self, settings: AISettings) -> None:
        """注入 AI 配置并初始化 HTTP Session。"""
        self.settings = settings
        self.session = requests.Session()
        self._do_request = retry(
            stop=stop_after_attempt(settings.max_retries),
            wait=wait_exponential(multiplier=2, min=2, max=30),
            reraise=True,
        )(self._do_request)

    def is_available(self) -> bool:
        """检查 base_url、api_key、model 是否均已配置。"""
        return bool(self.settings.base_url and self.settings.api_key and self.settings.model)

    def _do_request(self, body: dict[str, Any]) -> requests.Response:
        """执行 HTTP POST 请求（由 __init__ 中的 tenacity 动态装饰重试）。"""
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
        """组装提示词并请求模型，解析返回的 JSON 内容。"""
        if not self.is_available():
            return AIResponse(success=False, content={}, error="AI provider not configured")

        body = {
            "model": self.settings.model,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": self.TASK_PROMPTS.get(task, self.DEFAULT_PROMPT),
                },
                {
                    "role": "user",
                    "content": json.dumps({"task": task, "payload": payload}, ensure_ascii=False),
                },
            ],
        }
        try:
            response = self._do_request(body)
            raw = response.json()
            message = raw["choices"][0]["message"]["content"]
            message = self._extract_json_text(message)
            content = json.loads(message)
            return AIResponse(success=True, content=content, raw_text=message)
        except Exception as exc:  # pragma: no cover - network behavior
            return AIResponse(success=False, content={}, error=str(exc))

    @staticmethod
    def _extract_json_text(text: str) -> str:
        """从模型返回的文本中提取纯 JSON 字符串。

        部分 API 网关（如 meai.cloud）会将 JSON 包裹在 markdown
        代码块中（```json ... ```），或在前后添加换行符。
        """
        text = text.strip()
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text

    def append_audit_log(self, trace: DecisionTrace) -> None:
        """将决策轨迹以 JSON Lines 格式追加到审计日志文件。"""
        audit_path = Path(self.settings.audit_log_path)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(trace.to_dict(), ensure_ascii=False) + "\n")
