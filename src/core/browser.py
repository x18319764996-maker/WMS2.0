"""中文说明：本模块负责浏览器会话、上下文和页面生命周期管理。"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from core.artifacts import ArtifactManager
from core.config.models import AppConfig


class BrowserSessionManager:
    def __init__(self, config: AppConfig, artifact_manager: ArtifactManager) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.config = config
        self.artifact_manager = artifact_manager

    @contextmanager
    def page_session(self) -> Iterator[Page]:
        """中文说明：在 BrowserSessionManager 中执行与 page_session 相关的操作。"""
        self.artifact_manager.ensure_directories()
        with sync_playwright() as playwright:
            browser_type = getattr(playwright, self.config.execution.browser)
            # 中文说明：优先按配置选择 channel 或可执行文件，支持直接复用本机浏览器。
            launch_kwargs = {
                "headless": self.config.execution.headless,
                "slow_mo": self.config.execution.slow_mo,
            }
            if self.config.execution.channel:
                launch_kwargs["channel"] = self.config.execution.channel
            if self.config.execution.executable_path:
                launch_kwargs["executable_path"] = self.config.execution.executable_path
            browser: Browser = browser_type.launch(
                **launch_kwargs,
            )
            context: BrowserContext = browser.new_context(
                record_video_dir=str(self.artifact_manager.videos_dir),
            )
            # 中文说明：将默认等待时间统一沉淀到上下文级，减少页面层重复设置。
            context.set_default_timeout(self.config.execution.default_timeout_ms)
            context.set_default_navigation_timeout(self.config.execution.navigation_timeout_ms)
            page = context.new_page()
            try:
                yield page
            finally:
                context.close()
                browser.close()
