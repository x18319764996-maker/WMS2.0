"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from pathlib import Path

from core.config.loader import ConfigLoader


def test_project_contracts_load_default_config():
    """中文说明：执行与 test_project_contracts_load_default_config 相关的逻辑。"""
    project_root = Path(__file__).resolve().parents[2]
    config = ConfigLoader(project_root).load("test")
    assert config.environment == "test"
    assert config.ai.mode in {"enhanced", "hybrid", "disabled"}
    assert set(config.systems.keys()) == {"oms", "wms"}