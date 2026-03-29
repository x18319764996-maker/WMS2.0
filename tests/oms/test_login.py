"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

import pytest


@pytest.mark.e2e
@pytest.mark.oms
def test_oms_login(require_live_ui, oms_flow, app_config):
    """中文说明：执行与 test_oms_login 相关的逻辑。"""
    oms = app_config.systems["oms"]
    oms_flow.login(
        oms.base_url,
        oms.login_path,
        app_config.credentials.oms_username,
        app_config.credentials.oms_password,
    )