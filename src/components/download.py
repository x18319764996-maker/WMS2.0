from __future__ import annotations

from pathlib import Path

from components.base_component import BaseComponent


class DownloadComponent(BaseComponent):
    def expect_download(self, trigger_selector: str, target_path: str | Path) -> Path:
        with self.page.expect_download() as download_info:
            self.page.locator(trigger_selector).click()
        download = download_info.value
        download.save_as(str(target_path))
        return Path(target_path)