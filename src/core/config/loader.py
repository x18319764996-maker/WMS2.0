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
        self.project_root = project_root or Path(__file__).resolve().parents[3]
        self.config_dir = self.project_root / "config"

    def load(self, env_name: str | None = None) -> AppConfig:
        load_dotenv(self.project_root / ".env", override=False)
        target_env = env_name or os.getenv("TEST_ENV", "test")
        config_path = self.config_dir / f"{target_env}.yaml"
        if not config_path.exists():
            raise ConfigurationError(f"未找到环境配置文件: {config_path}")

        raw = self._read_yaml(config_path)
        raw["credentials"] = self._build_credentials().model_dump()
        raw["ai"] = self._build_ai_settings(raw.get("ai", {})).model_dump()
        raw["execution"] = self._apply_execution_overrides(raw.get("execution", {}))
        return AppConfig.model_validate(raw)

    def _read_yaml(self, path: Path) -> Dict[str, Any]:
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def _build_credentials(self) -> CredentialSettings:
        return CredentialSettings(
            oms_username=os.getenv("OMS_USERNAME", ""),
            oms_password=os.getenv("OMS_PASSWORD", ""),
            wms_username=os.getenv("WMS_USERNAME", ""),
            wms_password=os.getenv("WMS_PASSWORD", ""),
        )

    def _build_ai_settings(self, yaml_ai: Dict[str, Any]) -> AISettings:
        merged = dict(yaml_ai)
        merged["mode"] = os.getenv("AI_MODE", merged.get("mode", "enhanced"))
        merged["base_url"] = os.getenv("AI_BASE_URL", merged.get("base_url", ""))
        merged["api_key"] = os.getenv("AI_API_KEY", merged.get("api_key", ""))
        merged["model"] = os.getenv("AI_MODEL", merged.get("model", ""))
        merged["timeout_seconds"] = int(os.getenv("AI_TIMEOUT_SECONDS", merged.get("timeout_seconds", 20)))
        merged["max_retries"] = int(os.getenv("AI_MAX_RETRIES", merged.get("max_retries", 2)))
        return AISettings.model_validate(merged)

    def _apply_execution_overrides(self, yaml_execution: Dict[str, Any]) -> Dict[str, Any]:
        merged = dict(yaml_execution)
        explicit_headless = os.getenv("HEADLESS")
        if explicit_headless is not None:
            merged["headless"] = explicit_headless.lower() == "true"
        elif os.getenv("JENKINS_URL") or os.getenv("CI"):
            merged["headless"] = True
        return merged