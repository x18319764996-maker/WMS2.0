"""SelfHealingLocator 逻辑测试。"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from ai.locator import SelfHealingLocator
from ai.models import AIResponse, LocatorCandidate
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


@pytest.mark.ai
def test_rule_based_match_succeeds(mock_page: MagicMock, disabled_ai_settings: AISettings):
    """规则定位命中时直接返回，不触发 AI。"""
    # 让 #username 能命中
    def locator_side_effect(selector):
        loc = MagicMock()
        loc.count.return_value = 1 if selector == "#username" else 0
        return loc

    mock_page.locator.side_effect = locator_side_effect

    locator = SelfHealingLocator(disabled_ai_settings, provider=None)
    candidates = [LocatorCandidate("user", "#username")]
    resolution = locator.resolve(mock_page, candidates, "登录用户名")

    assert resolution.source == "rule"
    assert resolution.success is True
    assert resolution.selector == "#username"


@pytest.mark.ai
def test_rule_fails_ai_disabled(mock_page: MagicMock, disabled_ai_settings: AISettings):
    """规则全部失败 + AI 禁用时返回 success=False。"""
    locator = SelfHealingLocator(disabled_ai_settings, provider=None)
    candidates = [
        LocatorCandidate("wrong1", "#nonexistent"),
        LocatorCandidate("wrong2", ".also-wrong"),
    ]
    resolution = locator.resolve(mock_page, candidates, "不存在的元素")

    assert resolution.success is False
    assert resolution.source == "none"


@pytest.mark.ai
def test_candidates_not_exhausted(mock_page: MagicMock):
    """验证 BUG-2 修复：generator 候选在 AI 阶段仍可用。"""
    settings = AISettings(mode="enhanced", base_url="http://x", api_key="k", model="m")

    # mock provider
    mock_provider = MagicMock(spec=OpenAICompatibleProvider)
    mock_provider.is_available.return_value = True

    captured_payloads = []

    def capture_call(task, payload):
        captured_payloads.append(payload)
        return AIResponse(success=True, content={"selector": "#ai-fix"}, raw_text='{"selector":"#ai-fix"}')

    mock_provider.complete_json.side_effect = capture_call

    # 让 AI 返回的 selector 也命中
    def locator_side_effect(selector):
        loc = MagicMock()
        loc.count.return_value = 1 if selector == "#ai-fix" else 0
        return loc

    mock_page.locator.side_effect = locator_side_effect

    # 使用 generator（非 list），测试迭代器消耗修复
    def gen_candidates():
        yield LocatorCandidate("c1", "#wrong1")
        yield LocatorCandidate("c2", "#wrong2")

    locator = SelfHealingLocator(settings, provider=mock_provider)
    resolution = locator.resolve(mock_page, gen_candidates(), "测试迭代器")

    # AI 应收到非空候选列表
    assert len(captured_payloads) == 1
    assert len(captured_payloads[0]["candidates"]) == 2, "candidates 不应为空（BUG-2 修复验证）"
    assert resolution.source == "ai"
    assert resolution.success is True


@pytest.mark.ai
def test_ai_heals_with_valid_selector(mock_page: MagicMock):
    """mock Provider 返回有效 selector，二次校验通过。"""
    settings = AISettings(mode="enhanced", base_url="http://x", api_key="k", model="m")

    mock_provider = MagicMock(spec=OpenAICompatibleProvider)
    mock_provider.is_available.return_value = True
    mock_provider.complete_json.return_value = AIResponse(
        success=True, content={"selector": "#healed"}, raw_text='{"selector":"#healed"}'
    )

    def locator_side_effect(selector):
        loc = MagicMock()
        loc.count.return_value = 1 if selector == "#healed" else 0
        return loc

    mock_page.locator.side_effect = locator_side_effect

    locator = SelfHealingLocator(settings, provider=mock_provider)
    candidates = [LocatorCandidate("wrong", "#nonexistent")]
    resolution = locator.resolve(mock_page, candidates, "自愈测试")

    assert resolution.source == "ai"
    assert resolution.success is True
    assert resolution.selector == "#healed"


@pytest.mark.ai
def test_ai_selector_fails_verification(mock_page: MagicMock):
    """AI 返回 selector 但二次校验失败。"""
    settings = AISettings(mode="enhanced", base_url="http://x", api_key="k", model="m")

    mock_provider = MagicMock(spec=OpenAICompatibleProvider)
    mock_provider.is_available.return_value = True
    mock_provider.complete_json.return_value = AIResponse(
        success=True, content={"selector": "#bad-ai-guess"}, raw_text='{"selector":"#bad-ai-guess"}'
    )

    # 所有 locator 都返回 count=0（包括 AI 推荐的）
    locator = SelfHealingLocator(settings, provider=mock_provider)
    candidates = [LocatorCandidate("wrong", "#nonexistent")]
    resolution = locator.resolve(mock_page, candidates, "校验失败测试")

    assert resolution.source == "ai"
    assert resolution.success is False
