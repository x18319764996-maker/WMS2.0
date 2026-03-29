import pytest


@pytest.mark.e2e
@pytest.mark.wms
def test_wms_login_success(require_live_ui, wms_flow, app_config, live_page):
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
