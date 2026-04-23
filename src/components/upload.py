"""文件上传组件，封装文件输入控件的文件注入操作。"""

from __future__ import annotations

from pathlib import Path

from components.base_component import BaseComponent


class UploadComponent(BaseComponent):
    """文件上传组件，通过 set_input_files 向 file input 注入文件。"""

    def upload_file(self, input_selector: str, file_path: str | Path) -> None:
        """向文件上传 input 注入指定文件路径。"""
        self.page.locator(input_selector).set_input_files(str(file_path))