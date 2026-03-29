import pytest


@pytest.mark.e2e
@pytest.mark.cross_system
def test_wms_jump_to_oms_window(require_live_ui, cross_system_flow, app_config):
    wms = app_config.systems["wms"]
    jump_url = cross_system_flow.jump_from_wms_to_oms(wms.base_url)
    assert jump_url.startswith("http")
