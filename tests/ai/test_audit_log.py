"""审计日志写入测试。"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai.locator import SelfHealingLocator
from ai.models import DecisionTrace, LocatorCandidate
from ai.provider import OpenAICompatibleProvider
from core.config.models import AISettings


@pytest.mark.ai
def test_creates_file_and_appends(tmp_audit_path: Path):
    """两次 append 后文件有两行合法 JSON。"""
    settings = AISettings(mode="enhanced", audit_log_path=tmp_audit_path)
    provider = OpenAICompatibleProvider(settings)

    for i in range(2):
        trace = DecisionTrace(
            action="test_action",
            mode="enhanced",
            success=True,
            context_summary=f"test_{i}",
            result_summary=f"result_{i}",
        )
        provider.append_audit_log(trace)

    assert tmp_audit_path.exists()
    lines = tmp_audit_path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2

    for line in lines:
        data = json.loads(line)
        assert "action" in data
        assert "mode" in data
        assert "success" in data


@pytest.mark.ai
def test_directory_auto_created(tmp_path: Path):
    """深层路径自动创建。"""
    deep_path = tmp_path / "a" / "b" / "c" / "audit.jsonl"
    settings = AISettings(mode="enhanced", audit_log_path=deep_path)
    provider = OpenAICompatibleProvider(settings)

    trace = DecisionTrace(
        action="test", mode="enhanced", success=True,
        context_summary="deep", result_summary="ok",
    )
    provider.append_audit_log(trace)

    assert deep_path.exists()
    data = json.loads(deep_path.read_text(encoding="utf-8").strip())
    assert data["action"] == "test"


@pytest.mark.ai
def test_locator_resolve_writes_audit(mock_page: MagicMock, tmp_audit_path: Path):
    """SelfHealingLocator.resolve() 后审计文件有对应记录。"""
    settings = AISettings(mode="disabled", audit_log_path=tmp_audit_path)
    provider = OpenAICompatibleProvider(settings)
    locator = SelfHealingLocator(settings, provider=provider)

    # 让 #username 命中
    def locator_side_effect(selector):
        loc = MagicMock()
        loc.count.return_value = 1 if selector == "#username" else 0
        return loc

    mock_page.locator.side_effect = locator_side_effect

    candidates = [LocatorCandidate("user", "#username")]
    locator.resolve(mock_page, candidates, "审计测试")

    assert tmp_audit_path.exists()
    line = tmp_audit_path.read_text(encoding="utf-8").strip()
    data = json.loads(line)
    assert data["action"] == "resolve_locator"
    assert data["success"] is True
