import pytest


@pytest.mark.e2e
@pytest.mark.cross_system
def test_order_to_warehouse_full_flow(require_live_ui, cross_system_flow, app_config, data_loader, shared_store):
    oms = app_config.systems["oms"]
    wms = app_config.systems["wms"]
    case_data = data_loader.load_yaml("oms_orders.yaml")
    create_data = case_data["create_order"]

    context = cross_system_flow.run_order_to_warehouse(
        oms.base_url,
        wms.base_url,
        oms.login_path,
        wms.login_path,
        (app_config.credentials.oms_username, app_config.credentials.oms_password),
        (app_config.credentials.wms_username, app_config.credentials.wms_password),
        create_data["customer_name"],
        create_data["sku_code"],
        create_data["quantity"],
    )
    shared_store.put("cross_system_context", context)
    assert context.order_no.startswith("SO-")