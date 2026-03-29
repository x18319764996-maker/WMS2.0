"""中文说明：本模块用于巡检并修复 Python 文件中的问号乱码注释。"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[2]
SCAN_DIRS = [ROOT / "src", ROOT / "tests"]


def build_parser() -> argparse.ArgumentParser:
    """中文说明：构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(description="巡检并修复 Python 文件中的问号乱码注释")
    parser.add_argument("--check", action="store_true", help="只巡检，不写回修复")
    return parser


def iter_python_files() -> list[Path]:
    """中文说明：遍历项目中需要巡检的 Python 文件。"""
    files: list[Path] = []
    for base in SCAN_DIRS:
        for path in base.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            files.append(path)
    return files


def has_broken_comment(text: str) -> bool:
    """中文说明：仅检查注释和文档字符串中是否包含明显的问号乱码。"""
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#") and "???" in stripped:
            return True
        if stripped.startswith('"""') and "???" in stripped:
            return True
        if stripped.startswith("'''") and "???" in stripped:
            return True
    return False


def replace_many(text: str, replacements: dict[str, str]) -> str:
    """中文说明：按顺序批量替换文本片段。"""
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def fix_browser(text: str) -> str:
    """中文说明：修复 browser.py 中已知的乱码注释。"""
    return replace_many(
        text,
        {
            '"""涓枃璇存槑锛氭湰妯″潡璐熻矗娴忚鍣ㄤ細璇濄€佷笂涓嬫枃鍜岄〉闈㈢敓鍛藉懆鏈熺鐞嗐€?""': '"""中文说明：本模块负责浏览器会话、上下文和页面生命周期管理。"""',
            '"""涓枃璇存槑锛氬垵濮嬪寲褰撳墠瀵硅薄锛屽苟娉ㄥ叆璇ュ璞¤繍琛屾墍闇€鐨勪緷璧栥€?""': '"""中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""',
            '"""涓枃璇存槑锛氬湪 BrowserSessionManager 涓墽琛屼笌 page_session 鐩稿叧鐨勬搷浣溿€?""': '"""中文说明：在 BrowserSessionManager 中创建并管理单次页面会话。"""',
            '# 涓枃璇存槑锛氫紭鍏堟寜閰嶇疆閫夋嫨 channel 鎴栧彲鎵ц鏂囦欢锛屾敮鎸佺洿鎺ュ鐢ㄦ湰鏈烘祻瑙堝櫒銆?': '# 中文说明：优先按配置选择 channel 或可执行文件，支持直接复用本机浏览器。',
            '# 涓枃璇存槑锛氬皢榛樿绛夊緟鏃堕棿缁熶竴娌夋穩鍒颁笂涓嬫枃绾э紝鍑忓皯椤甸潰灞傞噸澶嶈缃€?': '# 中文说明：将默认等待时间统一沉淀到上下文级，减少页面层重复设置。',
        },
    )


def fix_loader(text: str) -> str:
    """中文说明：修复 loader.py 中已知的乱码注释。"""
    return replace_many(
        text,
        {
            '"""涓枃璇存槑锛氭湰鏂囦欢鏄」鐩腑鐨?Python 妯″潡锛岀敤浜庢壙杞藉搴旂殑鑷姩鍖栬兘鍔涙垨娴嬭瘯閫昏緫銆?""': '"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""',
            '"""涓枃璇存槑锛氬垵濮嬪寲褰撳墠瀵硅薄锛屽苟娉ㄥ叆璇ュ璞¤繍琛屾墍闇€鐨勪緷璧栥€?""': '"""中文说明：初始化当前对象，并注入该对象运行所需的依赖。"""',
            '"""涓枃璇存槑锛氬湪 ConfigLoader 涓姞杞戒笌 load 鐩稿叧鐨勬搷浣溿€?""': '"""中文说明：在 ConfigLoader 中加载指定环境的完整配置。"""',
            '"""涓枃璇存槑锛氬湪 ConfigLoader 涓鍙栦笌 _read_yaml 鐩稿叧鐨勬搷浣溿€?""': '"""中文说明：在 ConfigLoader 中读取指定 YAML 配置文件。"""',
            '"""涓枃璇存槑锛氬湪 ConfigLoader 涓瀯寤轰笌 _build_credentials 鐩稿叧鐨勬搷浣溿€?""': '"""中文说明：在 ConfigLoader 中组装账号与密码配置。"""',
            '"""涓枃璇存槑锛氬湪 ConfigLoader 涓瀯寤轰笌 _build_ai_settings 鐩稿叧鐨勬搷浣溿€?""': '"""中文说明：在 ConfigLoader 中合并并构建 AI 运行配置。"""',
            '"""涓枃璇存槑锛氬湪 ConfigLoader 涓簲鐢ㄤ笌 _apply_execution_overrides 鐩稿叧鐨勬搷浣溿€?""': '"""中文说明：在 ConfigLoader 中应用浏览器执行相关的运行时覆盖项。"""',
            '# 涓枃璇存槑锛氱粺涓€鎸夆€?env + YAML + 杩愯鏃剁幆澧冨彉閲忚鐩栤€濈殑椤哄簭鏋勫缓鏈€缁堥厤缃€?': '# 中文说明：统一按“.env + YAML + 运行时环境变量覆盖”的顺序构建最终配置。',
            '# 涓枃璇存槑锛欰I 閰嶇疆浼樺厛璇荤幆澧冨彉閲忥紝渚夸簬鍒囨崲涓嶅悓妯″瀷鏈嶅姟鍜岃繍琛屾ā寮忋€?': '# 中文说明：AI 配置优先读环境变量，便于切换不同模型服务和运行模式。',
            '# 涓枃璇存槑锛欳I/Jenkins 鍦烘櫙榛樿鏀逛负鏃犲ご锛岄伩鍏嶄緷璧栨闈㈢幆澧冦€?': '# 中文说明：CI/Jenkins 场景默认改为无头，避免依赖桌面环境。',
            'raise ConfigurationError(f"?????????: {config_path}")': 'raise ConfigurationError(f"未找到配置文件: {config_path}")',
        },
    )


def fix_runner(text: str) -> str:
    """中文说明：修复 run_all_scenarios.py 中已知的乱码注释。"""
    return replace_many(
        text,
        {
            '"""涓枃璇存槑锛氭湰妯″潡鎻愪緵缁熶竴杩愯鍏ュ彛锛岀敤涓€涓懡浠や覆琛屾墽琛屾墍鏈?E2E 鍦烘櫙銆?""': '"""中文说明：本模块提供统一运行入口，用一个命令串行执行所有 E2E 场景。"""',
            '"""涓枃璇存槑锛氭瀯寤轰笌 build_parser 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：构建统一运行入口的命令行参数解析器。"""',
            'description="缁熶竴鎵ц WMS/OMS UI 鑷姩鍖栧満鏅?)': 'description="统一执行 WMS/OMS UI 自动化场景")',
            'help="杩愯鐩爣锛屽彲閫夊€硷細all銆乷ms銆亀ms銆乧ross_system銆乻moke锛屾垨鐩存帴浼?tests 涓嬬殑鏂囦欢/鐩綍璺緞"': 'help="运行目标，可选值：all、oms、wms、cross_system、smoke，或直接传 tests 下的文件/目录路径"',
            'help="鎸?pytest -k 鍏抽敭瀛楄繃婊よ鎵ц鐨勫満鏅?,' : 'help="按 pytest -k 关键字过滤要执行的场景",',
            '"""涓枃璇存槑锛氳В鏋愪笌 resolve_target 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：把命令行目标映射为 pytest 需要执行的路径范围。"""',
            '# 涓枃璇存槑锛氳繖閲岀粺涓€缁存姢鐭洰鏍囧悕鍜屾祴璇曠洰褰曠殑鏄犲皠鍏崇郴锛屼究浜庡懡浠よ鐩存帴鎸夊煙杩愯銆??????????????????????????????': '# 中文说明：这里统一维护短目标名和测试目录的映射关系，便于命令行直接按域运行。',
            '"""????????????????????????????"""': '"""中文说明：组装 pytest 命令并执行统一场景入口。"""',
            '# 涓枃璇存槑锛氳繖閲岀粺涓€缁存姢鐭洰鏍囧悕鍜屾祴璇曠洰褰曠殑鏄犲皠鍏崇郴锛屼究浜庡懡浠よ鐩存帴鎸夊煙杩愯銆????????????????????????': '# 中文说明：统一注入默认环境变量，保证本地直接执行时具备最小运行上下文。',
            '# ????????? pytest ??????????????????????????': '# 中文说明：先拼装公共 pytest 参数，再根据目标和关键字补充过滤条件。',
            '# ?????? smoke ????????????????????': '# 中文说明：除 smoke 外，其余入口默认只执行标记为 e2e 的场景。',
            '# 涓枃璇存槑锛氳繖閲岀粺涓€缁存姢鐭洰鏍囧悕鍜屾祴璇曠洰褰曠殑鏄犲皠鍏崇郴锛屼究浜庡懡浠よ鐩存帴鎸夊煙杩愯銆?????????? pytest -k ???????': '# 中文说明：当用户提供关键字时，继续用 pytest -k 做更细粒度筛选。',
            '# 涓枃璇存槑锛氳繖閲岀粺涓€缁存姢鐭洰鏍囧悕鍜屾祴璇曠洰褰曠殑鏄犲皠鍏崇郴锛屼究浜庡懡浠よ鐩存帴鎸夊煙杩愯銆????????????????????????': '# 中文说明：最后补上目标路径范围，让统一入口只运行用户指定的场景集合。',
        },
    )


def fix_conftest(text: str) -> str:
    """中文说明：修复 conftest.py 中已知的乱码注释。"""
    return replace_many(
        text,
        {
            '"""涓枃璇存槑锛氭湰鏂囦欢鏄」鐩腑鐨?Python 妯″潡锛岀敤浜庢壙杞藉搴旂殑鑷姩鍖栬兘鍔涙垨娴嬭瘯閫昏緫銆?""': '"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 project_root 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：提供项目根目录夹具，供其余夹具统一复用。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 setup_logging 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：在测试会话启动时加载统一日志配置。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 app_config 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：加载当前测试环境对应的全局配置对象。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 artifact_manager 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：初始化测试产物管理器，并提前创建产物目录。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 data_loader 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：提供测试数据加载器，供业务流读取外部数据。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 shared_store 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：提供跨步骤共享运行态数据的存储对象。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 ai_provider 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：初始化 AI Provider，供定位和分析模块复用。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 locator_strategy 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：构建带自愈能力的统一定位策略对象。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 assertion_assistant 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：初始化断言助手，用于补充 AI 辅助校验能力。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 failure_analysis_agent 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：初始化失败分析代理，用于异常诊断和报告增强。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 oms_api_client 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：创建 OMS API 客户端，供 UI 与接口联合校验使用。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 wms_api_client 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：创建 WMS API 客户端，供 UI 与接口联合校验使用。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 browser_manager 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：提供浏览器会话管理器，统一负责页面生命周期。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 require_live_ui 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：在真实 UI 未开启时统一跳过依赖页面的用例。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 live_page 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：为每条真实用例提供独立页面会话。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 oms_flow 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：组装 OMS 业务流对象，供 OMS 场景直接调用。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 wms_flow 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：组装 WMS 业务流对象，供 WMS 场景直接调用。"""',
            '"""涓枃璇存槑锛氭墽琛屼笌 cross_system_flow 鐩稿叧鐨勯€昏緫銆?""': '"""中文说明：组装跨系统业务流对象，串联 OMS 与 WMS 的联动场景。"""',
            '# 涓枃璇存槑锛氭湭寮€鍚湡瀹?UI 鏃剁粺涓€鍦ㄨ繖閲岃烦杩囷紝閬垮厤姣忎釜鐢ㄤ緥閮介噸澶嶅垽鏂€?': '# 中文说明：未开启真实 UI 时统一在这里跳过，避免每个用例都重复判断。',
            'pytest.skip("??? ENABLE_LIVE_UI=true????? UI ??")': 'pytest.skip("请先设置 ENABLE_LIVE_UI=true 再执行真实 UI 用例")',
            '# 涓枃璇存槑锛氭湭寮€鍚湡瀹?UI 鏃剁粺涓€鍦ㄨ繖閲岃烦杩囷紝閬垮厤姣忎釜鐢ㄤ緥閮介噸澶嶅垽鏂€?????': '# 中文说明：为每条真实用例提供独立页面会话，保证不同场景之间相互隔离。',
        },
    )


FIXERS: dict[str, Callable[[str], str]] = {
    str(ROOT / "src" / "core" / "browser.py"): fix_browser,
    str(ROOT / "src" / "core" / "config" / "loader.py"): fix_loader,
    str(ROOT / "src" / "utils" / "run_all_scenarios.py"): fix_runner,
    str(ROOT / "tests" / "conftest.py"): fix_conftest,
}


def scan_files() -> list[Path]:
    """中文说明：扫描并返回仍存在问号乱码注释的文件列表。"""
    broken: list[Path] = []
    for path in iter_python_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        if has_broken_comment(text):
            broken.append(path)
    return broken


def repair_file(path: Path) -> bool:
    """中文说明：按已知修复规则修复单个文件。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    fixer = FIXERS.get(str(path))
    if fixer is None:
        return False
    repaired = fixer(text)
    if repaired == text:
        return False
    path.write_text(repaired, encoding="utf-8", newline="")
    return True


def main() -> int:
    """中文说明：执行巡检或修复流程，并输出最终结果。"""
    args = build_parser().parse_args()
    broken = scan_files()
    if not broken:
        print("未发现问号乱码注释文件。")
        return 0

    print("发现以下文件存在问号乱码注释：")
    for path in broken:
        print(path.relative_to(ROOT))

    if args.check:
        return 1

    repaired_count = 0
    for path in broken:
        if repair_file(path):
            repaired_count += 1

    print(f"已修复文件数量：{repaired_count}")
    remaining = scan_files()
    if remaining:
        print("仍有文件包含问号乱码注释：")
        for path in remaining:
            print(path.relative_to(ROOT))
        return 2

    print("所有问号乱码注释已修复。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
