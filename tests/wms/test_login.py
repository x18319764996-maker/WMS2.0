"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

import pytest


@pytest.mark.e2e
@pytest.mark.wms
def test_wms_login_success(require_live_ui, wms_flow, app_config, live_page):
    """中文说明：执行与 test_wms_login_success 相关的逻辑。"""
    wms = app_config.systems["wms"]
    wms_flow.login(
        wms.base_url,
        wms.login_path,
        app_config.credentials.wms_username,
        app_config.credentials.wms_password,
    )
    live_page.wait_for_url("**/dropshipping/home", timeout=30000)
    assert "/dropshipping/home" in live_page.url
    assert "首页" in live_page.locator("body").inner_text()
