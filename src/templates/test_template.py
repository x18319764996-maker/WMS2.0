import pytest


@pytest.mark.e2e
def test_example_flow(require_live_ui, example_flow, app_config):
    example_flow.run(app_config.systems["oms"].base_url)