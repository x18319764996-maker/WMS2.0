from pathlib import Path

from core.config.loader import ConfigLoader


def test_project_contracts_load_default_config():
    project_root = Path(__file__).resolve().parents[2]
    config = ConfigLoader(project_root).load("test")
    assert config.environment == "test"
    assert config.ai.mode in {"enhanced", "hybrid", "disabled"}
    assert set(config.systems.keys()) == {"oms", "wms"}