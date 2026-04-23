"""业务流脚手架模板，新建业务流时可复制此文件并按需修改。"""

from __future__ import annotations

from flows.base_flow import BaseFlow


class ExampleFlow(BaseFlow):
    """示例业务流，演示页面注入和流执行的基本结构。"""

    def __init__(self, example_page, assertion_assistant, failure_analysis_agent) -> None:
        """注入示例页面和 AI 辅助组件。"""
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.example_page = example_page

    def run(self, base_url: str) -> None:
        """打开示例页面并执行操作。"""
        self.example_page.open_page(base_url)
        self.example_page.do_action()