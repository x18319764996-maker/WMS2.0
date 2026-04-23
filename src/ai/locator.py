"""定位器策略与 AI 自愈定位实现。

规则优先（rule-based）策略会依次尝试候选 selector；
当全部失败且 AI 可用时，将页面 DOM 片段提交给大模型推断最优 selector，
并在真实页面上二次校验可用性。
"""

from __future__ import annotations

from typing import Iterable

from playwright.sync_api import Page

from dataclasses import asdict

from ai.models import DecisionTrace, LocatorCandidate, LocatorResolution
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


class LocatorStrategy:
    """定位策略抽象基类，定义 resolve 接口供不同策略实现。"""

    def resolve(self, page: Page, candidates: Iterable[LocatorCandidate], context: str) -> LocatorResolution:
        """解析定位候选，返回可用的 selector 与决策轨迹。"""
        raise NotImplementedError


class SelfHealingLocator(LocatorStrategy):
    """自愈定位器，实现三阶段决策流：规则候选匹配 → AI 推断 → 真实页面二次校验。

    当所有规则候选失败且 AI 可用时，提取页面 DOM 片段调用大模型推断最优 selector，
    并在真实页面上验证其有效性。全程记录决策轨迹到审计日志。
    """

    def __init__(self, ai_settings: AISettings, provider: OpenAICompatibleProvider | None = None) -> None:
        """注入 AI 配置与可选的 Provider。"""
        self.ai_settings = ai_settings
        self.provider = provider

    def resolve(self, page: Page, candidates: Iterable[LocatorCandidate], context: str) -> LocatorResolution:
        """依次尝试候选定位；失败时调用 AI 推断并回校结果。"""
        candidates = list(candidates)
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
            "candidates": [asdict(candidate) for candidate in candidates],
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
        """判断 selector 在当前页面是否命中至少一个元素。"""
        if not selector:
            return False
        try:
            return page.locator(selector).count() > 0
        except Exception:
            return False

    def _audit(self, trace: DecisionTrace) -> None:
        """将决策轨迹追加到审计日志（如配置了 provider）。"""
        if self.provider:
            self.provider.append_audit_log(trace)
