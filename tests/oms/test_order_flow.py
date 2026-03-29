"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

import pytest


@pytest.mark.e2e
@pytest.mark.oms
def test_oms_create_and_search_order(require_live_ui, oms_flow, app_config, data_loader, shared_store):
    """中文说明：执行与 test_oms_create_and_search_order 相关的逻辑。"""
    oms = app_config.systems["oms"]
    case_data = data_loader.load_yaml("oms_orders.yaml")
    create_data = case_data["create_order"]
    oms_flow.login(
        oms.base_url,
        oms.login_path,
        app_config.credentials.oms_username,
        app_config.credentials.oms_password,
    )
    order_no = oms_flow.create_order(
        oms.base_url,
        create_data["customer_name"],
        create_data["sku_code"],
        create_data["quantity"],
    )
    shared_store.put("order_no", order_no)
    oms_flow.search_order(oms.base_url, order_no)
    order_detail = oms_flow.fetch_order_detail(order_no)
    assert isinstance(order_detail, dict)
