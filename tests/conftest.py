"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

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
    """中文说明：执行与 project_root 相关的逻辑。"""
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def setup_logging(project_root: Path) -> None:
    """中文说明：执行与 setup_logging 相关的逻辑。"""
    configure_logging(project_root / "config" / "logging.yaml")


@pytest.fixture(scope="session")
def app_config(project_root: Path):
    """中文说明：执行与 app_config 相关的逻辑。"""
    return ConfigLoader(project_root).load(os.getenv("TEST_ENV", "test"))


@pytest.fixture(scope="session")
def artifact_manager(project_root: Path, app_config):
    """中文说明：执行与 artifact_manager 相关的逻辑。"""
    manager = ArtifactManager(project_root, app_config.reporting)
    manager.ensure_directories()
    return manager


@pytest.fixture(scope="session")
def data_loader(project_root: Path):
    """中文说明：执行与 data_loader 相关的逻辑。"""
    return TestDataLoader(project_root / "src" / "data" / "testdata")


@pytest.fixture(scope="session")
def shared_store():
    """中文说明：执行与 shared_store 相关的逻辑。"""
    return SharedStore()


@pytest.fixture(scope="session")
def ai_provider(app_config):
    """中文说明：执行与 ai_provider 相关的逻辑。"""
    return OpenAICompatibleProvider(app_config.ai)


@pytest.fixture(scope="session")
def locator_strategy(app_config, ai_provider):
    """中文说明：执行与 locator_strategy 相关的逻辑。"""
    return SelfHealingLocator(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def assertion_assistant(app_config, ai_provider):
    """中文说明：执行与 assertion_assistant 相关的逻辑。"""
    return AssertionAssistant(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def failure_analysis_agent(app_config, ai_provider):
    """中文说明：执行与 failure_analysis_agent 相关的逻辑。"""
    return FailureAnalysisAgent(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def oms_api_client(app_config):
    """中文说明：执行与 oms_api_client 相关的逻辑。"""
    return OMSApiClient(app_config.systems["oms"], app_config.api)


@pytest.fixture(scope="session")
def wms_api_client(app_config):
    """中文说明：执行与 wms_api_client 相关的逻辑。"""
    return WMSApiClient(app_config.systems["wms"], app_config.api)


@pytest.fixture(scope="session")
def browser_manager(app_config, artifact_manager):
    """中文说明：执行与 browser_manager 相关的逻辑。"""
    return BrowserSessionManager(app_config, artifact_manager)


@pytest.fixture()
def require_live_ui():
    """中文说明：执行与 require_live_ui 相关的逻辑。"""
    if not is_live_ui_enabled():
        # 中文说明：未开启真实 UI 时统一在这里跳过，避免每个用例都重复判断。
        pytest.skip("??? ENABLE_LIVE_UI=true????? UI ??")


@pytest.fixture()
def live_page(browser_manager, require_live_ui):
    """中文说明：执行与 live_page 相关的逻辑。"""
    # 中文说明：未开启真实 UI 时统一在这里跳过，避免每个用例都重复判断。?????
    with browser_manager.page_session() as page:
        yield page


@pytest.fixture()
def oms_flow(live_page, locator_strategy, oms_api_client, assertion_assistant, failure_analysis_agent):
    """中文说明：执行与 oms_flow 相关的逻辑。"""
    return OMSOrderFlow(
        OMSLoginPage(live_page, locator_strategy),
        OMSOrderPage(live_page, locator_strategy),
        oms_api_client,
        assertion_assistant,
        failure_analysis_agent,
    )


@pytest.fixture()
def wms_flow(live_page, locator_strategy, wms_api_client, assertion_assistant, failure_analysis_agent):
    """中文说明：执行与 wms_flow 相关的逻辑。"""
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
    """中文说明：执行与 cross_system_flow 相关的逻辑。"""
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
