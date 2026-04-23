"""业务流基类。

所有跨页面的高级业务流程（如登录->入库->出库）继承此类，
统一持有断言助手与失败分析代理，便于在流级别做 AI 增强的异常处理。
"""

from __future__ import annotations

from ai.assertion import AssertionAssistant
from ai.failure_analysis import FailureAnalysisAgent


class BaseFlow:
    """业务流基类，持有断言助手和失败分析代理，提供流级别的 AI 增强异常处理能力。"""

    def __init__(self, assertion_assistant: AssertionAssistant, failure_analysis_agent: FailureAnalysisAgent) -> None:
        """注入断言助手与失败分析代理。"""
        self.assertion_assistant = assertion_assistant
        self.failure_analysis_agent = failure_analysis_agent