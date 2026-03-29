from __future__ import annotations

from flows.base_flow import BaseFlow


class ExampleFlow(BaseFlow):
    def __init__(self, example_page, assertion_assistant, failure_analysis_agent) -> None:
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.example_page = example_page

    def run(self, base_url: str) -> None:
        self.example_page.open_page(base_url)
        self.example_page.do_action()