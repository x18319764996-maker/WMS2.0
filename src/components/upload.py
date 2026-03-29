from __future__ import annotations

from pathlib import Path

from components.base_component import BaseComponent


class UploadComponent(BaseComponent):
    def upload_file(self, input_selector: str, file_path: str | Path) -> None:
        self.page.locator(input_selector).set_input_files(str(file_path))