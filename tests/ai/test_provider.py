"""Provider 连通性与核心逻辑测试。"""

from __future__ import annotations

import json

import pytest

from ai.models import AIResponse
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


@pytest.mark.ai
def test_glm_api_connectivity(real_provider: OpenAICompatibleProvider):
    """验证 GLM API 可达且返回合法 JSON 响应。"""
    response = real_provider.complete_json(
        "heal_locator",
        {
            "context": "测试连通性",
            "candidates": [],
            "dom_excerpt": "<div id='test'>hello</div>",
        },
    )
    assert response.success is True, f"API 调用失败: {response.error}"
    assert isinstance(response.content, dict)
    assert response.raw_text != ""


@pytest.mark.ai
def test_provider_not_configured():
    """base_url 为空时返回 success=False。"""
    settings = AISettings(mode="enhanced", base_url="", api_key="", model="")
    provider = OpenAICompatibleProvider(settings)
    response = provider.complete_json("heal_locator", {"context": "test"})
    assert response.success is False
    assert "not configured" in response.error


@pytest.mark.ai
def test_provider_is_available_check():
    """缺少 url/key/model 任一要素时 is_available 返回 False。"""
    cases = [
        {"base_url": "", "api_key": "key", "model": "model"},
        {"base_url": "http://x", "api_key": "", "model": "model"},
        {"base_url": "http://x", "api_key": "key", "model": ""},
    ]
    for kwargs in cases:
        settings = AISettings(mode="enhanced", **kwargs)
        provider = OpenAICompatibleProvider(settings)
        assert provider.is_available() is False, f"应为 False: {kwargs}"


@pytest.mark.ai
def test_provider_json_response_format(real_provider: OpenAICompatibleProvider):
    """验证 GLM 返回内容可正常 JSON 序列化。"""
    response = real_provider.complete_json(
        "failure_analysis",
        {
            "step_name": "test_step",
            "error": "TimeoutError: 超时",
            "extra_context": {},
            "snapshot": "<html><body>test</body></html>",
        },
    )
    assert response.success is True, f"API 调用失败: {response.error}"
    # 验证 content 可序列化
    serialized = json.dumps(response.content, ensure_ascii=False)
    assert len(serialized) > 2  # 不是空对象 "{}"
