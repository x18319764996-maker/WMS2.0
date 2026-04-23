"""日志配置工具，从 YAML 加载日志格式或降级为 basicConfig。"""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml


def configure_logging(config_path: Path) -> None:
    """从 YAML 配置文件加载日志格式；文件不存在时降级为 basicConfig。"""
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as file:
            logging.config.dictConfig(yaml.safe_load(file))
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def get_logger(name: str) -> logging.Logger:
    """按名称获取 Logger 实例，用于模块级日志输出。"""
    return logging.getLogger(name)