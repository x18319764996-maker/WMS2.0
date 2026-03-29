from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from core.artifacts import ArtifactManager
from core.config.models import AppConfig


class BrowserSessionManager:
    def __init__(self, config: AppConfig, artifact_manager: ArtifactManager) -> None:
        self.config = config
        self.artifact_manager = artifact_manager

    @contextmanager
    def page_session(self) -> Iterator[Page]:
        self.artifact_manager.ensure_directories()
        with sync_playwright() as playwright:
            browser_type = getattr(playwright, self.config.execution.browser)
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
            context.set_default_timeout(self.config.execution.default_timeout_ms)
            context.set_default_navigation_timeout(self.config.execution.navigation_timeout_ms)
            page = context.new_page()
            try:
                yield page
            finally:
                context.close()
                browser.close()
