"""AI 模块测试专用 fixtures。"""

from __future__ import annotations

import json
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from playwright.sync_api import Page

from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


@pytest.fixture(scope="session")
def ai_settings() -> AISettings:
    """从项目配置加载真实 AISettings（GLM-4.7）。"""
    from core.config.loader import ConfigLoader

    project_root = Path(__file__).resolve().parents[2]
    config = ConfigLoader(project_root).load()
    return config.ai


@pytest.fixture()
def disabled_ai_settings() -> AISettings:
    """构造一个 AI 功能禁用的配置。"""
    return AISettings(mode="disabled")


@pytest.fixture(scope="session")
def real_provider(ai_settings: AISettings) -> OpenAICompatibleProvider:
    """基于真实 GLM 配置创建 Provider。"""
    return OpenAICompatibleProvider(ai_settings)


@pytest.fixture(autouse=True)
def _rate_limit_guard(request):
    """在调用真实 API 的测试之间添加间隔，避免 429 限流。"""
    yield
    # 检查测试是否使用了 real_provider fixture（即可能调用了真实 API）
    if "real_provider" in request.fixturenames:
        time.sleep(2)


@pytest.fixture()
def mock_page() -> MagicMock:
    """构造一个可控的 mock Playwright Page 对象。"""
    page = MagicMock(spec=Page)

    # 默认 DOM 内容：模拟 WMS 登录页面
    page.content.return_value = (
        '<html><body>'
        '<form id="loginForm">'
        '<input id="username" name="username" type="text" placeholder="用户名">'
        '<input id="password" name="password" type="password" placeholder="密码">'
        '<button type="submit">登录</button>'
        '</form>'
        '</body></html>'
    )

    # 默认所有 locator 返回 count=0（可在具体测试中覆盖）
    mock_locator = MagicMock()
    mock_locator.count.return_value = 0
    page.locator.return_value = mock_locator

    return page


@pytest.fixture()
def tmp_audit_path(tmp_path: Path) -> Path:
    """提供临时审计日志路径。"""
    return tmp_path / "audit" / "ai_decisions.jsonl"
