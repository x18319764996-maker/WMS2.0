from __future__ import annotations

from pathlib import Path
from typing import Dict

from pydantic import BaseModel, Field


class SystemEndpoint(BaseModel):
    base_url: str
    login_path: str


class ExecutionSettings(BaseModel):
    browser: str = "chromium"
    channel: str = ""
    executable_path: str = ""
    headless: bool = False
    slow_mo: int = 0
    default_timeout_ms: int = 10_000
    action_timeout_ms: int = 12_000
    navigation_timeout_ms: int = 20_000
    retry_count: int = 1


class ReportingSettings(BaseModel):
    artifact_root: Path = Path("artifacts")
    screenshot_dir: str = "screenshots"
    video_dir: str = "videos"
    log_dir: str = "logs"
    html_report: Path = Path("artifacts/reports/pytest-report.html")
    allure_dir: Path = Path("allure-results")


class AISettings(BaseModel):
    mode: str = "enhanced"
    semantic_snapshot_limit: int = 8000
    allow_runtime_decision: bool = True
    audit_log_path: Path = Path("artifacts/logs/ai_decisions.jsonl")
    base_url: str = ""
    api_key: str = ""
    model: str = ""
    timeout_seconds: int = 20
    max_retries: int = 2


class ApiSettings(BaseModel):
    timeout_seconds: int = 15
    oms_endpoints: Dict[str, str] = Field(default_factory=dict)
    wms_endpoints: Dict[str, str] = Field(default_factory=dict)


class CredentialSettings(BaseModel):
    oms_username: str = ""
    oms_password: str = ""
    wms_username: str = ""
    wms_password: str = ""


class AppConfig(BaseModel):
    environment: str
    systems: Dict[str, SystemEndpoint]
    execution: ExecutionSettings
    reporting: ReportingSettings
    ai: AISettings
    api: ApiSettings
    credentials: CredentialSettings
