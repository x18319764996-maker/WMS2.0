"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml


def configure_logging(config_path: Path) -> None:
    """中文说明：执行与 configure_logging 相关的逻辑。"""
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as file:
            logging.config.dictConfig(yaml.safe_load(file))
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def get_logger(name: str) -> logging.Logger:
    """中文说明：获取与 get_logger 相关的逻辑。"""
    return logging.getLogger(name)