"""AI 配置加载测试。"""

from __future__ import annotations

from pathlib import Path

import pytest

from core.config.loader import ConfigLoader
from core.config.models import AISettings


@pytest.mark.ai
def test_default_ai_settings():
    """AISettings 默认值正确。"""
    settings = AISettings()
    assert settings.mode == "enhanced"
    assert settings.max_retries == 2
    assert settings.timeout_seconds == 20
    assert settings.semantic_snapshot_limit == 8000


@pytest.mark.ai
def test_env_overrides_yaml(monkeypatch):
    """环境变量 AI_MODE=disabled 覆盖 YAML 中的 enhanced。"""
    monkeypatch.setenv("AI_MODE", "disabled")
    monkeypatch.setenv("TEST_ENV", "test")
    project_root = Path(__file__).resolve().parents[2]
    config = ConfigLoader(project_root).load("test")
    assert config.ai.mode == "disabled"


@pytest.mark.ai
def test_max_retries_from_env(monkeypatch):
    """AI_MAX_RETRIES=5 能被正确加载。"""
    monkeypatch.setenv("AI_MAX_RETRIES", "5")
    monkeypatch.setenv("TEST_ENV", "test")
    project_root = Path(__file__).resolve().parents[2]
    config = ConfigLoader(project_root).load("test")
    assert config.ai.max_retries == 5
