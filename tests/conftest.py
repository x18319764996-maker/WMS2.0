from __future__ import annotations

import os
from pathlib import Path

import pytest

from ai.assertion import AssertionAssistant
from ai.failure_analysis import FailureAnalysisAgent
from ai.locator import SelfHealingLocator
from ai.provider import OpenAICompatibleProvider
from api.oms_client import OMSApiClient
from api.wms_client import WMSApiClient
from core.artifacts import ArtifactManager
from core.browser import BrowserSessionManager
from core.config.loader import ConfigLoader
from core.logging_utils import configure_logging
from data.loader import TestDataLoader
from data.shared_store import SharedStore
from flows.cross_system.order_fulfillment_flow import CrossSystemOrderFulfillmentFlow
from flows.oms.order_flow import OMSOrderFlow
from flows.wms.warehouse_flow import WMSWarehouseFlow
from pages.oms.login_page import OMSLoginPage
from pages.oms.order_page import OMSOrderPage
from pages.wms.customer_profile_page import WMSCustomerProfilePage
from pages.wms.inbound_page import WMSInboundPage
from pages.wms.inventory_page import WMSInventoryPage
from pages.wms.login_page import WMSLoginPage
from pages.wms.outbound_page import WMSOutboundPage
from utils.runtime import is_live_ui_enabled


@pytest.fixture(scope="session")
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def setup_logging(project_root: Path) -> None:
    configure_logging(project_root / "config" / "logging.yaml")


@pytest.fixture(scope="session")
def app_config(project_root: Path):
    return ConfigLoader(project_root).load(os.getenv("TEST_ENV", "test"))


@pytest.fixture(scope="session")
def artifact_manager(project_root: Path, app_config):
    manager = ArtifactManager(project_root, app_config.reporting)
    manager.ensure_directories()
    return manager


@pytest.fixture(scope="session")
def data_loader(project_root: Path):
    return TestDataLoader(project_root / "src" / "data" / "testdata")


@pytest.fixture(scope="session")
def shared_store():
    return SharedStore()


@pytest.fixture(scope="session")
def ai_provider(app_config):
    return OpenAICompatibleProvider(app_config.ai)


@pytest.fixture(scope="session")
def locator_strategy(app_config, ai_provider):
    return SelfHealingLocator(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def assertion_assistant(app_config, ai_provider):
    return AssertionAssistant(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def failure_analysis_agent(app_config, ai_provider):
    return FailureAnalysisAgent(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def oms_api_client(app_config):
    return OMSApiClient(app_config.systems["oms"], app_config.api)


@pytest.fixture(scope="session")
def wms_api_client(app_config):
    return WMSApiClient(app_config.systems["wms"], app_config.api)


@pytest.fixture(scope="session")
def browser_manager(app_config, artifact_manager):
    return BrowserSessionManager(app_config, artifact_manager)


@pytest.fixture()
def require_live_ui():
    if not is_live_ui_enabled():
        pytest.skip("未开启 ENABLE_LIVE_UI=true，跳过真实 UI 执行")


@pytest.fixture()
def live_page(browser_manager, require_live_ui):
    with browser_manager.page_session() as page:
        yield page


@pytest.fixture()
def oms_flow(live_page, locator_strategy, oms_api_client, assertion_assistant, failure_analysis_agent):
    return OMSOrderFlow(
        OMSLoginPage(live_page, locator_strategy),
        OMSOrderPage(live_page, locator_strategy),
        oms_api_client,
        assertion_assistant,
        failure_analysis_agent,
    )


@pytest.fixture()
def wms_flow(live_page, locator_strategy, wms_api_client, assertion_assistant, failure_analysis_agent):
    return WMSWarehouseFlow(
        WMSLoginPage(live_page, locator_strategy),
        WMSInboundPage(live_page, locator_strategy),
        WMSInventoryPage(live_page, locator_strategy),
        WMSOutboundPage(live_page, locator_strategy),
        wms_api_client,
        assertion_assistant,
        failure_analysis_agent,
    )


@pytest.fixture()
def cross_system_flow(live_page, locator_strategy, oms_api_client, wms_api_client, assertion_assistant, failure_analysis_agent):
    oms_flow = OMSOrderFlow(
        OMSLoginPage(live_page, locator_strategy),
        OMSOrderPage(live_page, locator_strategy),
        oms_api_client,
        assertion_assistant,
        failure_analysis_agent,
    )
    wms_flow = WMSWarehouseFlow(
        WMSLoginPage(live_page, locator_strategy),
        WMSInboundPage(live_page, locator_strategy),
        WMSInventoryPage(live_page, locator_strategy),
        WMSOutboundPage(live_page, locator_strategy),
        wms_api_client,
        assertion_assistant,
        failure_analysis_agent,
    )
    return CrossSystemOrderFulfillmentFlow(
        oms_flow,
        wms_flow,
        WMSCustomerProfilePage(live_page, locator_strategy),
        assertion_assistant,
        failure_analysis_agent,
    )