"""下载组件，封装点击触发下载并保存文件的操作。"""

from __future__ import annotations

from pathlib import Path

from components.base_component import BaseComponent


class DownloadComponent(BaseComponent):
    """文件下载组件，等待浏览器下载事件并将文件保存到指定路径。"""

    def expect_download(self, trigger_selector: str, target_path: str | Path) -> Path:
        """点击触发下载并将文件保存到指定路径，返回保存后的 Path。"""
        with self.page.expect_download() as download_info:
            self.page.locator(trigger_selector).click()
        download = download_info.value
        download.save_as(str(target_path))
        return Path(target_path)