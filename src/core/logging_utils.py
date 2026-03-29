from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml


def configure_logging(config_path: Path) -> None:
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as file:
            logging.config.dictConfig(yaml.safe_load(file))
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)