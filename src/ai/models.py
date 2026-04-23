"""AI 模块数据结构定义。

包含模型响应、决策轨迹、定位候选/结果和失败分析等 dataclass，
贯穿 provider → locator → assertion → failure_analysis 全链路。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class AIResponse:
    """模型调用的统一响应体，封装成功/失败状态、解析后的 JSON 内容和原始文本。"""

    success: bool
    content: dict[str, Any]  # 中文说明：解析后的 JSON 结构，失败时为空 dict
    raw_text: str = ""  # 中文说明：模型返回的原始文本内容
    error: str = ""  # 中文说明：失败时的错误描述


@dataclass(slots=True)
class DecisionTrace:
    """AI 决策轨迹记录，用于审计日志和问题追溯。"""

    action: str  # 中文说明：决策动作类型，如 resolve_locator / failure_analysis
    mode: str  # 中文说明：AI 运行模式（enhanced / disabled）
    success: bool
    context_summary: str  # 中文说明：决策发生时的业务上下文摘要
    result_summary: str  # 中文说明：决策结果的文本描述
    fallback_action: str = ""  # 中文说明：失败时的兜底动作标识
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """将决策轨迹序列化为字典，供审计日志 JSON 输出。"""
        return asdict(self)


@dataclass(slots=True)
class LocatorCandidate:
    """定位候选项，包含候选名称、CSS 选择器和类型标识。"""

    name: str  # 中文说明：候选名称，如 "id_selector" / "data_testid"
    selector: str  # 中文说明：CSS 选择器字符串
    kind: str = "locator"


@dataclass(slots=True)
class LocatorResolution:
    """定位解析结果，记录最终选中的 selector 及其来源（rule / ai）。"""

    selector: str
    source: str  # 中文说明：定位来源，rule=规则命中 / ai=AI推断 / none=未命中
    success: bool
    trace: DecisionTrace


@dataclass(slots=True)
class FailureAnalysis:
    """失败分析结果，包含根因、修复建议和分类标签。"""

    step_name: str  # 中文说明：失败步骤名称
    probable_cause: str  # 中文说明：推断的根本原因
    suggestion: str  # 中文说明：可操作的修复建议
    classification: str  # 中文说明：分类标签（timeout/ui_failure/network_error/data_mismatch/unknown）
    trace: DecisionTrace