from __future__ import annotations

from datetime import datetime
from pathlib import Path

from core.config.models import ReportingSettings


class ArtifactManager:
    def __init__(self, project_root: Path, reporting: ReportingSettings) -> None:
        self.project_root = project_root
        self.reporting = reporting
        self.root = project_root / reporting.artifact_root
        self.logs_dir = self.root / reporting.log_dir
        self.screenshots_dir = self.root / reporting.screenshot_dir
        self.videos_dir = self.root / reporting.video_dir
        self.reports_dir = reporting.html_report.parent if reporting.html_report.is_absolute() else project_root / reporting.html_report.parent

    def ensure_directories(self) -> None:
        for path in [self.root, self.logs_dir, self.screenshots_dir, self.videos_dir, self.reports_dir]:
            path.mkdir(parents=True, exist_ok=True)

    def timestamped_file(self, category: str, stem: str, suffix: str) -> Path:
        base_dir = {
            "log": self.logs_dir,
            "screenshot": self.screenshots_dir,
            "video": self.videos_dir,
            "report": self.reports_dir,
        }[category]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return base_dir / f"{stem}_{timestamp}{suffix}"