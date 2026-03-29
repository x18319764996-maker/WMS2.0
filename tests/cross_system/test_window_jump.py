"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

import pytest


@pytest.mark.e2e
@pytest.mark.cross_system
def test_wms_jump_to_oms_window(require_live_ui, cross_system_flow, app_config):
    """中文说明：执行与 test_wms_jump_to_oms_window 相关的逻辑。"""
    wms = app_config.systems["wms"]
    jump_url = cross_system_flow.jump_from_wms_to_oms(wms.base_url)
    assert jump_url.startswith("http")
