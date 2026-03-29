"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

import pytest


@pytest.mark.e2e
def test_example_flow(require_live_ui, example_flow, app_config):
    """中文说明：执行与 test_example_flow 相关的逻辑。"""
    example_flow.run(app_config.systems["oms"].base_url)