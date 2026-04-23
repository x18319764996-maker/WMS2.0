"""测试用例脚手架模板，新建测试文件时可复制此文件并按需修改。"""

import pytest


@pytest.mark.e2e
def test_example_flow(require_live_ui, example_flow, app_config):
    """示例测试：调用示例业务流验证端到端流程。"""
    example_flow.run(app_config.systems["oms"].base_url)