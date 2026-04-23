"""WMS+OMS AI UI 自动化框架主入口。

提供统一的 CLI 命令：
    python main.py run [target]     运行测试场景
    python main.py check            检查运行环境
    python main.py report           打开最新测试报告
"""

from __future__ import annotations

import argparse
import os
import sys
import webbrowser
from pathlib import Path

# 确保 src 目录在路径中，以便直接运行 python main.py
project_root = Path(__file__).resolve().parent
src_path = str(project_root / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from utils.run_all_scenarios import main as run_main


def cmd_run(argv: list[str] | None) -> int:
    """委托给统一的 pytest 场景执行器。"""
    return run_main(argv)


def cmd_check() -> int:
    """检查项目运行所需的最小环境。"""
    issues = 0
    project_root = Path(__file__).resolve().parent

    # 1. .env 文件
    env_file = project_root / ".env"
    if env_file.exists():
        print("[OK] .env 文件已存在")
    else:
        print("[WARN] .env 文件不存在，将使用 config/*.yaml 中的默认值")
        issues += 1

    # 2. Playwright 浏览器
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browsers = ["chromium", "firefox", "webkit"]
            for browser in browsers:
                try:
                    getattr(p, browser).launch()
                    print(f"[OK] Playwright {browser} 浏览器可用")
                except Exception:
                    print(f"[WARN] Playwright {browser} 未安装，建议执行: playwright install {browser}")
                    issues += 1
    except Exception as exc:
        print(f"[ERROR] Playwright 检查失败: {exc}")
        issues += 1

    # 3. AI 配置（可选）
    ai_base = os.getenv("AI_BASE_URL", "")
    if ai_base:
        print(f"[OK] AI_BASE_URL 已配置: {ai_base}")
    else:
        print("[INFO] AI_BASE_URL 未配置，AI 自愈/断言助手将处于禁用状态（不影响基础 UI 测试）")

    # 4. 产物目录
    for sub in ("artifacts/screenshots", "artifacts/videos", "artifacts/logs", "artifacts/reports"):
        (project_root / sub).mkdir(parents=True, exist_ok=True)
    print("[OK] 产物目录已就绪")

    if issues:
        print(f"\n发现 {issues} 项待处理，请根据提示补充配置。")
    else:
        print("\n环境检查通过，可以开始运行测试。")
    return issues


def cmd_report() -> int:
    """尝试打开最新的 pytest HTML 报告。"""
    report_path = Path(__file__).resolve().parent / "artifacts" / "reports" / "pytest-report.html"
    if report_path.exists():
        webbrowser.open(report_path.as_uri())
        print(f"已打开报告: {report_path}")
        return 0
    print(f"报告不存在: {report_path}")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wms-oms-ai-ui-automation",
        description="WMS+OMS AI 增强型 UI 自动化框架",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="运行测试场景（同 run-all-scenarios）")
    run_parser.add_argument("target", nargs="?", default="all", help="运行目标，如 all / oms / wms / smoke")
    run_parser.add_argument("-k", "--keyword", default="", help="pytest -k 关键字过滤")

    sub.add_parser("check", help="检查运行环境")
    sub.add_parser("report", help="打开最新 HTML 报告")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return cmd_run([args.target] + (["-k", args.keyword] if args.keyword else []))
    if args.command == "check":
        return cmd_check()
    if args.command == "report":
        return cmd_report()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
