"""OMS 订单创建→搜索→API 查询全流程测试。"""

import pytest


@pytest.mark.e2e
@pytest.mark.oms
def test_oms_create_and_search_order(require_live_ui, oms_flow, app_config, data_loader, shared_store):
    """验证 OMS 创建订单→搜索订单→API 查询订单详情的完整流程。"""
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
