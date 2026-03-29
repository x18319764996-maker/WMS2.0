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
    """中文说明：提供项目根目录夹具，供其余夹具统一复用。"""
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def setup_logging(project_root: Path) -> None:
    """中文说明：在测试会话启动时加载统一日志配置。"""
    configure_logging(project_root / "config" / "logging.yaml")


@pytest.fixture(scope="session")
def app_config(project_root: Path):
    """中文说明：加载当前测试环境对应的全局配置对象。"""
    return ConfigLoader(project_root).load(os.getenv("TEST_ENV", "test"))


@pytest.fixture(scope="session")
def artifact_manager(project_root: Path, app_config):
    """中文说明：初始化测试产物管理器，并提前创建产物目录。"""
    manager = ArtifactManager(project_root, app_config.reporting)
    manager.ensure_directories()
    return manager


@pytest.fixture(scope="session")
def data_loader(project_root: Path):
    """中文说明：提供测试数据加载器，供业务流读取外部数据。"""
    return TestDataLoader(project_root / "src" / "data" / "testdata")


@pytest.fixture(scope="session")
def shared_store():
    """中文说明：提供跨步骤共享运行态数据的存储对象。"""
    return SharedStore()


@pytest.fixture(scope="session")
def ai_provider(app_config):
    """中文说明：初始化 AI Provider，供定位和分析模块复用。"""
    return OpenAICompatibleProvider(app_config.ai)


@pytest.fixture(scope="session")
def locator_strategy(app_config, ai_provider):
    """中文说明：构建带自愈能力的统一定位策略对象。"""
    return SelfHealingLocator(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def assertion_assistant(app_config, ai_provider):
    """中文说明：初始化断言助手，用于补充 AI 辅助校验能力。"""
    return AssertionAssistant(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def failure_analysis_agent(app_config, ai_provider):
    """中文说明：初始化失败分析代理，用于异常诊断和报告增强。"""
    return FailureAnalysisAgent(app_config.ai, ai_provider)


@pytest.fixture(scope="session")
def oms_api_client(app_config):
    """中文说明：创建 OMS API 客户端，供 UI 与接口联合校验使用。"""
    return OMSApiClient(app_config.systems["oms"], app_config.api)


@pytest.fixture(scope="session")
def wms_api_client(app_config):
    """中文说明：创建 WMS API 客户端，供 UI 与接口联合校验使用。"""
    return WMSApiClient(app_config.systems["wms"], app_config.api)


@pytest.fixture(scope="session")
def browser_manager(app_config, artifact_manager):
    """中文说明：提供浏览器会话管理器，统一负责页面生命周期。"""
    return BrowserSessionManager(app_config, artifact_manager)


@pytest.fixture()
def require_live_ui():
    """中文说明：在真实 UI 未开启时统一跳过依赖页面的用例。"""
    if not is_live_ui_enabled():
        # 中文说明：未开启真实 UI 时统一在这里跳过，避免每个用例都重复判断。
        pytest.skip("请先设置 ENABLE_LIVE_UI=true 再执行真实 UI 用例")


@pytest.fixture()
def live_page(browser_manager, require_live_ui):
    """中文说明：为每条真实用例提供独立页面会话。"""
    # 中文说明：为每条真实用例提供独立页面会话，保证不同场景之间相互隔离。
    with browser_manager.page_session() as page:
        yield page


@pytest.fixture()
def oms_flow(live_page, locator_strategy, oms_api_client, assertion_assistant, failure_analysis_agent):
    """中文说明：组装 OMS 业务流对象，供 OMS 场景直接调用。"""
    return OMSOrderFlow(
        OMSLoginPage(live_page, locator_strategy),
        OMSOrderPage(live_page, locator_strategy),
        oms_api_client,
        assertion_assistant,
        failure_analysis_agent,
    )


@pytest.fixture()
def wms_flow(live_page, locator_strategy, wms_api_client, assertion_assistant, failure_analysis_agent):
    """中文说明：组装 WMS 业务流对象，供 WMS 场景直接调用。"""
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
    """中文说明：组装跨系统业务流对象，串联 OMS 与 WMS 的联动场景。"""
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
