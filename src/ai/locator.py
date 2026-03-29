"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from typing import Iterable

from playwright.sync_api import Page

from ai.models import DecisionTrace, LocatorCandidate, LocatorResolution
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


class LocatorStrategy:
    def resolve(self, page: Page, candidates: Iterable[LocatorCandidate], context: str) -> LocatorResolution:
        """中文说明：在 LocatorStrategy 中解析与 resolve 相关的操作。"""
        raise NotImplementedError


class SelfHealingLocator(LocatorStrategy):
    def __init__(self, ai_settings: AISettings, provider: OpenAICompatibleProvider | None = None) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.ai_settings = ai_settings
        self.provider = provider

    def resolve(self, page: Page, candidates: Iterable[LocatorCandidate], context: str) -> LocatorResolution:
        """中文说明：在 SelfHealingLocator 中解析与 resolve 相关的操作。"""
        for candidate in candidates:
            if self._matches(page, candidate.selector):
                # 中文说明：只要规则定位命中，就直接返回，不进入 AI 自愈分支。
                trace = DecisionTrace(
                    action="resolve_locator",
                    mode=self.ai_settings.mode,
                    success=True,
                    context_summary=context,
                    result_summary=f"规则定位命中: {candidate.selector}",
                    metadata={"source": "rule", "candidate": candidate.name},
                )
                self._audit(trace)
                return LocatorResolution(candidate.selector, "rule", True, trace)

        if self.ai_settings.mode == "disabled" or not self.provider or not self.provider.is_available():
            # 中文说明：AI 被关闭或 provider 不可用时，保留失败轨迹，便于后续排查。
            trace = DecisionTrace(
                action="resolve_locator",
                mode=self.ai_settings.mode,
                success=False,
                context_summary=context,
                result_summary="未命中规则定位，且 AI 未启用或不可用",
                fallback_action="raise_locator_error",
            )
            self._audit(trace)
            return LocatorResolution("", "none", False, trace)

        payload = {
            "context": context,
            "candidates": [candidate.__dict__ for candidate in candidates],
            "dom_excerpt": page.content()[: self.ai_settings.semantic_snapshot_limit],
        }
        response = self.provider.complete_json("heal_locator", payload)
        selector = response.content.get("selector", "") if response.success else ""
        success = bool(selector and self._matches(page, selector))
        # 中文说明：即使 AI 给出 selector，也必须回到真实页面中校验是否可用。
        trace = DecisionTrace(
            action="resolve_locator",
            mode=self.ai_settings.mode,
            success=success,
            context_summary=context,
            result_summary=response.raw_text or response.error or "AI 未返回结果",
            fallback_action="use_ai_selector" if success else "raise_locator_error",
            metadata={"source": "ai", "selector": selector},
        )
        self._audit(trace)
        return LocatorResolution(selector, "ai", success, trace)

    def _matches(self, page: Page, selector: str) -> bool:
        """中文说明：在 SelfHealingLocator 中判断与 _matches 相关的操作。"""
        if not selector:
            return False
        try:
            return page.locator(selector).count() > 0
        except Exception:
            return False

    def _audit(self, trace: DecisionTrace) -> None:
        """中文说明：在 SelfHealingLocator 中执行与 _audit 相关的操作。"""
        if self.provider:
            self.provider.append_audit_log(trace)
