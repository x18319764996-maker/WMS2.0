from __future__ import annotations

from typing import Any

from playwright.sync_api import Page

from ai.models import DecisionTrace, FailureAnalysis
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


class FailureAnalysisAgent:
    def __init__(self, settings: AISettings, provider: OpenAICompatibleProvider | None = None) -> None:
        self.settings = settings
        self.provider = provider

    def analyze(self, page: Page | None, step_name: str, error: Exception, extra_context: dict[str, Any] | None = None) -> FailureAnalysis:
        snapshot = ""
        if page:
            try:
                snapshot = page.content()[: self.settings.semantic_snapshot_limit]
            except Exception:
                snapshot = "page snapshot unavailable"

        if self.settings.mode != "disabled" and self.provider and self.provider.is_available():
            response = self.provider.complete_json(
                "failure_analysis",
                {
                    "step_name": step_name,
                    "error": str(error),
                    "extra_context": extra_context or {},
                    "snapshot": snapshot,
                },
            )
            content = response.content if response.success else {}
            probable_cause = content.get("probable_cause", str(error))
            suggestion = content.get("suggestion", "请检查 locator、接口数据和环境稳定性")
            classification = content.get("classification", "unknown")
            result_summary = response.raw_text or response.error or probable_cause
        else:
            probable_cause = str(error)
            if "Timeout" in str(error):
                classification = "timeout"
                suggestion = "优先检查等待策略、页面加载状态和 locator 稳定性"
            else:
                classification = "ui_failure"
                suggestion = "优先检查 locator、页面结构变更和测试数据"
            result_summary = probable_cause

        trace = DecisionTrace(
            action="failure_analysis",
            mode=self.settings.mode,
            success=True,
            context_summary=step_name,
            result_summary=result_summary,
            metadata={"classification": classification},
        )
        if self.provider:
            self.provider.append_audit_log(trace)
        return FailureAnalysis(step_name, probable_cause, suggestion, classification, trace)