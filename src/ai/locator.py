from __future__ import annotations

from typing import Iterable

from playwright.sync_api import Page

from ai.models import DecisionTrace, LocatorCandidate, LocatorResolution
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


class LocatorStrategy:
    def resolve(self, page: Page, candidates: Iterable[LocatorCandidate], context: str) -> LocatorResolution:
        raise NotImplementedError


class SelfHealingLocator(LocatorStrategy):
    def __init__(self, ai_settings: AISettings, provider: OpenAICompatibleProvider | None = None) -> None:
        self.ai_settings = ai_settings
        self.provider = provider

    def resolve(self, page: Page, candidates: Iterable[LocatorCandidate], context: str) -> LocatorResolution:
        for candidate in candidates:
            if self._matches(page, candidate.selector):
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
        if not selector:
            return False
        try:
            return page.locator(selector).count() > 0
        except Exception:
            return False

    def _audit(self, trace: DecisionTrace) -> None:
        if self.provider:
            self.provider.append_audit_log(trace)