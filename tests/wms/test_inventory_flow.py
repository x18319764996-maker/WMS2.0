"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

import pytest


@pytest.mark.e2e
@pytest.mark.wms
def test_wms_inbound_inventory_and_outbound(require_live_ui, wms_flow, app_config, data_loader):
    """中文说明：执行与 test_wms_inbound_inventory_and_outbound 相关的逻辑。"""
    wms = app_config.systems["wms"]
    case_data = data_loader.load_yaml("wms_operations.yaml")
    wms_flow.login(
        wms.base_url,
        wms.login_path,
        app_config.credentials.wms_username,
        app_config.credentials.wms_password,
    )
    wms_flow.create_inbound(wms.base_url, case_data["inbound"]["receipt_no"], case_data["inbound"]["sku_code"])
    wms_flow.query_inventory(wms.base_url, case_data["inventory"]["sku_code"])
    wms_flow.create_outbound(wms.base_url, case_data["outbound"]["outbound_no"], case_data["outbound"]["sku_code"])
    inventory_result = wms_flow.fetch_inventory(case_data["inventory"]["sku_code"])
    assert isinstance(inventory_result, dict)
