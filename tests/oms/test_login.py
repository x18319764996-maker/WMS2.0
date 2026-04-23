"""OMS 登录功能测试。"""

import pytest


@pytest.mark.e2e
@pytest.mark.oms
def test_oms_login(require_live_ui, oms_flow, app_config):
    """验证 OMS 用户登录流程。"""
    oms = app_config.systems["oms"]
    oms_flow.login(
        oms.base_url,
        oms.login_path,
        app_config.credentials.oms_username,
        app_config.credentials.oms_password,
    )