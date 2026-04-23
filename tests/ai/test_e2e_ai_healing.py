"""E2E AI 自愈定位测试。

在真实浏览器页面上验证：当所有规则候选定位器失败时，
AI 能否通过分析 DOM 片段推断出正确的 selector。
"""

from __future__ import annotations

import os

import pytest

from ai.locator import SelfHealingLocator
from ai.models import LocatorCandidate
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


@pytest.mark.ai
@pytest.mark.e2e
def test_ai_self_healing_on_real_page(
    require_live_ui,
    browser_manager,
    ai_settings: AISettings,
    real_provider: OpenAICompatibleProvider,
):
    """在 WMS 登录页上验证 AI 自愈定位能力。"""
    if ai_settings.mode == "disabled":
        pytest.skip("AI_MODE is disabled")
    if not real_provider.is_available():
        pytest.skip("AI provider not configured")

    locator = SelfHealingLocator(ai_settings, provider=real_provider)

    with browser_manager.page_session() as page:
        # 导航到 WMS 登录页
        page.goto("http://test.wms-v2.eccang.com/auth/login")
        page.wait_for_load_state("domcontentloaded")
        page.locator("#username").wait_for(state="visible", timeout=30000)

        # 构造故意错误的候选定位器
        wrong_candidates = [
            LocatorCandidate("wrong-id", "#nonexistent_username_field"),
            LocatorCandidate("wrong-class", ".wrong-class-name-xyz"),
        ]

        # AI 应能通过分析真实 DOM 推断出正确的用户名输入框 selector
        resolution = locator.resolve(page, wrong_candidates, "WMS 登录页面的用户名输入框")

        assert resolution.source == "ai", f"期望走 AI 路径，实际 source={resolution.source}"
        assert resolution.success is True, (
            f"AI 自愈失败，selector={resolution.selector!r}，"
            f"trace={resolution.trace.result_summary}"
        )
        assert page.locator(resolution.selector).count() > 0, (
            f"AI 返回的 selector '{resolution.selector}' 在真实页面上未命中"
        )
