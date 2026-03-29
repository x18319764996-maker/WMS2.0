from __future__ import annotations

from ai.assertion import AssertionAssistant
from ai.failure_analysis import FailureAnalysisAgent


class BaseFlow:
    def __init__(self, assertion_assistant: AssertionAssistant, failure_analysis_agent: FailureAnalysisAgent) -> None:
        self.assertion_assistant = assertion_assistant
        self.failure_analysis_agent = failure_analysis_agent