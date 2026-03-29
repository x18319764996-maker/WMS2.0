"""中文说明：本模块封装下载类操作，便于统一处理下载行为。"""

from __future__ import annotations

from pathlib import Path

from components.base_component import BaseComponent


class DownloadComponent(BaseComponent):
    def expect_download(self, trigger_selector: str, target_path: str | Path) -> Path:
        """中文说明：在 DownloadComponent 中断言校验与 expect_download 相关的操作。"""
        with self.page.expect_download() as download_info:
            self.page.locator(trigger_selector).click()
        download = download_info.value
        download.save_as(str(target_path))
        return Path(target_path)