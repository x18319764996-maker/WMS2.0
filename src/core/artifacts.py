"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from core.config.models import ReportingSettings


class ArtifactManager:
    def __init__(self, project_root: Path, reporting: ReportingSettings) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.project_root = project_root
        self.reporting = reporting
        self.root = project_root / reporting.artifact_root
        self.logs_dir = self.root / reporting.log_dir
        self.screenshots_dir = self.root / reporting.screenshot_dir
        self.videos_dir = self.root / reporting.video_dir
        self.reports_dir = reporting.html_report.parent if reporting.html_report.is_absolute() else project_root / reporting.html_report.parent

    def ensure_directories(self) -> None:
        """中文说明：在 ArtifactManager 中执行与 ensure_directories 相关的操作。"""
        for path in [self.root, self.logs_dir, self.screenshots_dir, self.videos_dir, self.reports_dir]:
            path.mkdir(parents=True, exist_ok=True)

    def timestamped_file(self, category: str, stem: str, suffix: str) -> Path:
        """中文说明：在 ArtifactManager 中执行与 timestamped_file 相关的操作。"""
        base_dir = {
            "log": self.logs_dir,
            "screenshot": self.screenshots_dir,
            "video": self.videos_dir,
            "report": self.reports_dir,
        }[category]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return base_dir / f"{stem}_{timestamp}{suffix}"