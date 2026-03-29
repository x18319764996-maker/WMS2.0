"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

from flows.base_flow import BaseFlow


class ExampleFlow(BaseFlow):
    def __init__(self, example_page, assertion_assistant, failure_analysis_agent) -> None:
        """中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""
        super().__init__(assertion_assistant, failure_analysis_agent)
        self.example_page = example_page

    def run(self, base_url: str) -> None:
        """中文说明：在 ExampleFlow 中执行与 run 相关的操作。"""
        self.example_page.open_page(base_url)
        self.example_page.do_action()