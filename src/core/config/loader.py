"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

from core.config.models import AISettings, AppConfig, CredentialSettings
from core.exceptions import ConfigurationError


class ConfigLoader:
    """Loads .env and YAML configuration and applies runtime overrides."""

    def __init__(self, project_root: Path | None = None) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.project_root = project_root or Path(__file__).resolve().parents[3]
        self.config_dir = self.project_root / "config"

    def load(self, env_name: str | None = None) -> AppConfig:
        """中文说明：在 ConfigLoader 中加载与 load 相关的操作。"""
        # 中文说明：统一按“.env + YAML + 运行时环境变量覆盖”的顺序构建最终配置。
        load_dotenv(self.project_root / ".env", override=False)
        target_env = env_name or os.getenv("TEST_ENV", "test")
        config_path = self.config_dir / f"{target_env}.yaml"
        if not config_path.exists():
            raise ConfigurationError(f"?????????: {config_path}")

        raw = self._read_yaml(config_path)
        raw["credentials"] = self._build_credentials().model_dump()
        raw["ai"] = self._build_ai_settings(raw.get("ai", {})).model_dump()
        raw["execution"] = self._apply_execution_overrides(raw.get("execution", {}))
        return AppConfig.model_validate(raw)

    def _read_yaml(self, path: Path) -> Dict[str, Any]:
        """中文说明：在 ConfigLoader 中读取与 _read_yaml 相关的操作。"""
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def _build_credentials(self) -> CredentialSettings:
        """中文说明：在 ConfigLoader 中构建与 _build_credentials 相关的操作。"""
        return CredentialSettings(
            oms_username=os.getenv("OMS_USERNAME", ""),
            oms_password=os.getenv("OMS_PASSWORD", ""),
            wms_username=os.getenv("WMS_USERNAME", ""),
            wms_password=os.getenv("WMS_PASSWORD", ""),
        )

    def _build_ai_settings(self, yaml_ai: Dict[str, Any]) -> AISettings:
        """中文说明：在 ConfigLoader 中构建与 _build_ai_settings 相关的操作。"""
        # 中文说明：AI 配置优先读环境变量，便于切换不同模型服务和运行模式。
        merged = dict(yaml_ai)
        merged["mode"] = os.getenv("AI_MODE", merged.get("mode", "enhanced"))
        merged["base_url"] = os.getenv("AI_BASE_URL", merged.get("base_url", ""))
        merged["api_key"] = os.getenv("AI_API_KEY", merged.get("api_key", ""))
        merged["model"] = os.getenv("AI_MODEL", merged.get("model", ""))
        merged["timeout_seconds"] = int(os.getenv("AI_TIMEOUT_SECONDS", merged.get("timeout_seconds", 20)))
        merged["max_retries"] = int(os.getenv("AI_MAX_RETRIES", merged.get("max_retries", 2)))
        return AISettings.model_validate(merged)

    def _apply_execution_overrides(self, yaml_execution: Dict[str, Any]) -> Dict[str, Any]:
        """中文说明：在 ConfigLoader 中应用与 _apply_execution_overrides 相关的操作。"""
        merged = dict(yaml_execution)
        if os.getenv("BROWSER_CHANNEL"):
            merged["channel"] = os.getenv("BROWSER_CHANNEL", "")
        if os.getenv("BROWSER_EXECUTABLE_PATH"):
            merged["executable_path"] = os.getenv("BROWSER_EXECUTABLE_PATH", "")
        explicit_headless = os.getenv("HEADLESS")
        if explicit_headless is not None:
            merged["headless"] = explicit_headless.lower() == "true"
        elif os.getenv("JENKINS_URL") or os.getenv("CI"):
            # 中文说明：CI/Jenkins 场景默认改为无头，避免依赖桌面环境。
            merged["headless"] = True
        return merged
