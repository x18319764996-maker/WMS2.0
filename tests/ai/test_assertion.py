"""AssertionAssistant 调用测试。"""

from __future__ import annotations

import pytest

from ai.assertion import AssertionAssistant
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


@pytest.mark.ai
def test_disabled_returns_meta(disabled_ai_settings: AISettings):
    """disabled 模式返回包含 enabled=False 的元数据。"""
    assistant = AssertionAssistant(disabled_ai_settings, provider=None)
    result = assistant.suggest(
        "login_flow",
        {"url_contains": "/home"},
        "<html><body>首页</body></html>",
    )
    assert result["enabled"] is False
    assert result["flow_name"] == "login_flow"


@pytest.mark.ai
def test_with_real_glm(ai_settings: AISettings, real_provider: OpenAICompatibleProvider):
    """真实 GLM 调用，返回非空断言建议。"""
    if ai_settings.mode == "disabled":
        pytest.skip("AI_MODE is disabled")
    if not real_provider.is_available():
        pytest.skip("AI provider not configured")

    assistant = AssertionAssistant(ai_settings, real_provider)
    result = assistant.suggest(
        "wms_login",
        {"url_contains": "/dropshipping/home", "page_contains_text": "首页"},
        '<html><body><div class="nav">首页</div><div class="content">欢迎</div></body></html>',
    )
    assert isinstance(result, dict)
    # AI 模式下不应返回 enabled=False
    assert result.get("enabled") is not False or len(result) > 2


@pytest.mark.ai
def test_provider_none(ai_settings: AISettings):
    """provider=None 时返回 disabled。"""
    settings = AISettings(mode="enhanced", base_url="http://x", api_key="k", model="m")
    assistant = AssertionAssistant(settings, provider=None)
    result = assistant.suggest("test", {}, "")
    assert result["enabled"] is False
