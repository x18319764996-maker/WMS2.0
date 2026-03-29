"""中文说明：本模块封装上传类控件的文件注入操作。"""

from __future__ import annotations

from pathlib import Path

from components.base_component import BaseComponent


class UploadComponent(BaseComponent):
    def upload_file(self, input_selector: str, file_path: str | Path) -> None:
        """中文说明：在 UploadComponent 中上传与 upload_file 相关的操作。"""
        self.page.locator(input_selector).set_input_files(str(file_path))