"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class AIResponse:
    success: bool
    content: dict[str, Any]
    raw_text: str = ""
    error: str = ""


@dataclass(slots=True)
class DecisionTrace:
    action: str
    mode: str
    success: bool
    context_summary: str
    result_summary: str
    fallback_action: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """中文说明：在 DecisionTrace 中执行与 to_dict 相关的操作。"""
        return asdict(self)


@dataclass(slots=True)
class LocatorCandidate:
    name: str
    selector: str
    kind: str = "locator"


@dataclass(slots=True)
class LocatorResolution:
    selector: str
    source: str
    success: bool
    trace: DecisionTrace


@dataclass(slots=True)
class FailureAnalysis:
    step_name: str
    probable_cause: str
    suggestion: str
    classification: str
    trace: DecisionTrace