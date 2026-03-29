"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from ai.assertion import AssertionAssistant
from ai.failure_analysis import FailureAnalysisAgent


class BaseFlow:
    def __init__(self, assertion_assistant: AssertionAssistant, failure_analysis_agent: FailureAnalysisAgent) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        self.assertion_assistant = assertion_assistant
        self.failure_analysis_agent = failure_analysis_agent