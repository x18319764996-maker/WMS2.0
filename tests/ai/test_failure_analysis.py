"""FailureAnalysisAgent 逻辑测试。"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from playwright.sync_api import Page

from ai.failure_analysis import FailureAnalysisAgent
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


@pytest.mark.ai
def test_local_fallback_timeout(disabled_ai_settings: AISettings):
    """Timeout 异常走本地兜底，classification='timeout'。"""
    agent = FailureAnalysisAgent(disabled_ai_settings, provider=None)
    error = TimeoutError("Timeout 30000ms exceeded waiting for selector")
    analysis = agent.analyze(None, "click_login_button", error)

    assert analysis.classification == "timeout"
    assert "等待策略" in analysis.suggestion
    assert analysis.step_name == "click_login_button"


@pytest.mark.ai
def test_local_fallback_ui_failure(disabled_ai_settings: AISettings):
    """非 Timeout 异常走本地兜底，classification='ui_failure'。"""
    agent = FailureAnalysisAgent(disabled_ai_settings, provider=None)
    error = LookupError("页面定位失败: username | 用户名输入框")
    analysis = agent.analyze(None, "fill_username", error)

    assert analysis.classification == "ui_failure"
    assert "locator" in analysis.suggestion


@pytest.mark.ai
def test_ai_path_with_real_glm(
    ai_settings: AISettings, real_provider: OpenAICompatibleProvider, mock_page: MagicMock
):
    """真实 GLM 诊断，返回有意义的 cause/suggestion。"""
    if ai_settings.mode == "disabled":
        pytest.skip("AI_MODE is disabled")
    if not real_provider.is_available():
        pytest.skip("AI provider not configured")

    agent = FailureAnalysisAgent(ai_settings, real_provider)
    error = TimeoutError("Timeout 10000ms exceeded waiting for selector '#submit-btn'")
    analysis = agent.analyze(mock_page, "click_submit", error)

    assert analysis.probable_cause != ""
    assert analysis.suggestion != ""
    assert analysis.classification in {"timeout", "ui_failure", "network_error", "data_mismatch", "unknown"}


@pytest.mark.ai
def test_page_none_handled(disabled_ai_settings: AISettings):
    """page=None 时不抛异常，正常返回分析结果。"""
    agent = FailureAnalysisAgent(disabled_ai_settings, provider=None)
    error = RuntimeError("unexpected error")
    analysis = agent.analyze(None, "some_step", error)

    assert analysis.step_name == "some_step"
    assert analysis.classification in {"timeout", "ui_failure"}


@pytest.mark.ai
def test_page_content_exception(disabled_ai_settings: AISettings):
    """page.content() 抛异常时优雅降级。"""
    page = MagicMock(spec=Page)
    page.content.side_effect = RuntimeError("browser disconnected")

    agent = FailureAnalysisAgent(disabled_ai_settings, provider=None)
    error = LookupError("element not found")
    analysis = agent.analyze(page, "broken_page_step", error)

    assert analysis.step_name == "broken_page_step"
    assert analysis.classification == "ui_failure"
