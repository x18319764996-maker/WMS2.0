"""全局配置数据模型定义。

使用 Pydantic BaseModel 描述系统端点、执行参数、报告路径、AI 设置、
API 设置、凭据和总配置等结构，供 ConfigLoader 校验与注入。
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from pydantic import BaseModel, Field


class SystemEndpoint(BaseModel):
    """被测系统的访问端点，包含基础地址和登录路径。"""

    base_url: str  # 中文说明：系统根 URL，如 https://wms.example.com
    login_path: str  # 中文说明：登录页面的相对路径


class ExecutionSettings(BaseModel):
    """浏览器执行参数，控制浏览器类型、超时和重试策略。"""

    browser: str = "chromium"  # 中文说明：浏览器引擎，支持 chromium/firefox/webkit
    channel: str = ""  # 中文说明：浏览器渠道，如 chrome、msedge
    executable_path: str = ""  # 中文说明：自定义浏览器可执行文件路径
    headless: bool = False  # 中文说明：是否无头模式运行（CI 环境建议开启）
    slow_mo: int = 0  # 中文说明：每步操作间隔毫秒数，调试时可设为 100-500
    default_timeout_ms: int = 10_000
    action_timeout_ms: int = 12_000
    navigation_timeout_ms: int = 20_000
    retry_count: int = 1  # 中文说明：用例失败后的重试次数


class ReportingSettings(BaseModel):
    """测试产物输出路径配置，包括截图、视频、日志和报告。"""

    artifact_root: Path = Path("artifacts")
    screenshot_dir: str = "screenshots"
    video_dir: str = "videos"
    log_dir: str = "logs"
    html_report: Path = Path("artifacts/reports/pytest-report.html")
    allure_dir: Path = Path("allure-results")


class AISettings(BaseModel):
    """AI 增强功能配置，控制模型端点、运行模式和审计日志。"""

    mode: str = "enhanced"  # 中文说明：AI 运行模式，disabled=关闭 / enhanced=增强
    semantic_snapshot_limit: int = 8000  # 中文说明：发送给模型的 DOM 片段最大字符数
    allow_runtime_decision: bool = True
    audit_log_path: Path = Path("artifacts/logs/ai_decisions.jsonl")
    base_url: str = ""  # 中文说明：OpenAI 兼容 API 地址
    api_key: str = ""
    model: str = ""  # 中文说明：模型名称，如 glm-5、gpt-4o
    timeout_seconds: int = 20
    max_retries: int = 2  # 中文说明：API 请求失败后的最大重试次数


class ApiSettings(BaseModel):
    """后端 API 接口配置，包含超时和 OMS/WMS 接口路径模板。"""

    timeout_seconds: int = 15
    oms_endpoints: Dict[str, str] = Field(default_factory=dict)  # 中文说明：OMS 接口名→路径模板映射
    wms_endpoints: Dict[str, str] = Field(default_factory=dict)  # 中文说明：WMS 接口名→路径模板映射


class CredentialSettings(BaseModel):
    """测试账号凭据，通常由环境变量注入。"""

    oms_username: str = ""
    oms_password: str = ""
    wms_username: str = ""
    wms_password: str = ""


class AppConfig(BaseModel):
    """应用全局配置根模型，聚合所有子配置项。"""

    environment: str  # 中文说明：当前环境标识，如 test / staging / prod
    systems: Dict[str, SystemEndpoint]  # 中文说明：被测系统映射，键为系统名（wms/oms）
    execution: ExecutionSettings
    reporting: ReportingSettings
    ai: AISettings
    api: ApiSettings
    credentials: CredentialSettings
