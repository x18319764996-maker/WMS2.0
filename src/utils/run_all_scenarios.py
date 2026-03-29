"""中文说明：本模块提供统一运行入口，用一个命令串行执行所有 E2E 场景。"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """中文说明：构建与 build_parser 相关的逻辑。"""
    parser = argparse.ArgumentParser(description="统一执行 WMS/OMS UI 自动化场景")
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        help="运行目标，可选值：all、oms、wms、cross_system、smoke，或直接传 tests 下的文件/目录路径",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        default="",
        help="按 pytest -k 关键字过滤要执行的场景",
    )
    return parser


def resolve_target(target: str) -> list[str]:
    """中文说明：解析与 resolve_target 相关的逻辑。"""
    # 中文说明：这里统一维护短目标名和测试目录的映射关系，便于命令行直接按域运行。??????????????????????????????
    target_map = {
        "all": [],
        "oms": ["tests/oms"],
        "wms": ["tests/wms"],
        "cross_system": ["tests/cross_system"],
        "smoke": ["tests/smoke"],
    }
    return target_map.get(target, [target])


def main(argv: list[str] | None = None) -> int:
    """????????????????????????????"""
    project_root = Path(__file__).resolve().parents[2]
    os.chdir(project_root)
    args = build_parser().parse_args(argv)

    # 中文说明：这里统一维护短目标名和测试目录的映射关系，便于命令行直接按域运行。????????????????????????
    os.environ.setdefault("ENABLE_LIVE_UI", "true")
    os.environ.setdefault("TEST_ENV", "test")
    os.environ.setdefault("AI_MODE", "disabled")

    # ????????? pytest ??????????????????????????
    command = [
        sys.executable,
        "-m",
        "pytest",
        "--html=artifacts/reports/pytest-report.html",
        "--self-contained-html",
    ]
    if args.target != "smoke":
        # ?????? smoke ?????????????????
        command.extend(["-m", "e2e"])
    if args.keyword:
        # 中文说明：这里统一维护短目标名和测试目录的映射关系，便于命令行直接按域运行。?????????? pytest -k ???????
        command.extend(["-k", args.keyword])
    # 中文说明：这里统一维护短目标名和测试目录的映射关系，便于命令行直接按域运行。????????????????????????
    command.extend(resolve_target(args.target))
    return subprocess.call(command, cwd=project_root)


if __name__ == "__main__":
    raise SystemExit(main())
