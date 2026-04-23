"""WMS2.0 AI 增强测试 - 带详细日志捕获的运行器。

该脚本会拦截所有 AI Provider 调用，记录完整的输入/输出/耗时，
运行完整测试套件后生成超详细的 Markdown 测试报告。
"""

from __future__ import annotations

import datetime
import json
import time
import traceback
from pathlib import Path
from unittest.mock import patch

import pytest

# ────────────────────── 全局日志收集器 ──────────────────────

AI_CALL_LOG: list[dict] = []
TEST_RESULTS: list[dict] = []


def intercepted_complete_json(original_fn, self, task, payload):
    """拦截 complete_json 调用，记录完整输入/输出/耗时。"""
    call_record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "task": task,
        "system_prompt": self.TASK_PROMPTS.get(task, self.DEFAULT_PROMPT),
        "model": self.settings.model,
        "base_url": self.settings.base_url,
        "payload_summary": {
            k: (v[:200] + "..." if isinstance(v, str) and len(v) > 200 else v)
            for k, v in payload.items()
        },
        "payload_full": payload,
    }

    start = time.time()
    try:
        result = original_fn(self, task, payload)
        elapsed = time.time() - start
        call_record["elapsed_seconds"] = round(elapsed, 3)
        call_record["success"] = result.success
        call_record["response_content"] = result.content
        call_record["raw_text"] = result.raw_text[:1000] if result.raw_text else ""
        call_record["error"] = result.error
    except Exception as exc:
        elapsed = time.time() - start
        call_record["elapsed_seconds"] = round(elapsed, 3)
        call_record["success"] = False
        call_record["error"] = str(exc)
        call_record["traceback"] = traceback.format_exc()
        raise
    finally:
        AI_CALL_LOG.append(call_record)

    return result


# ────────────────────── Pytest 插件 ──────────────────────

class AITestLogPlugin:
    """Pytest 插件：捕获每个测试的结果。"""

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            TEST_RESULTS.append({
                "nodeid": report.nodeid,
                "outcome": report.outcome,
                "duration": round(report.duration, 3),
                "longrepr": str(report.longrepr) if report.longrepr else "",
            })
        elif report.when == "setup" and report.skipped:
            TEST_RESULTS.append({
                "nodeid": report.nodeid,
                "outcome": "skipped",
                "duration": round(report.duration, 3),
                "longrepr": str(report.longrepr) if report.longrepr else "",
            })


# ────────────────────── 主执行逻辑 ──────────────────────

def main():
    project_root = Path(__file__).resolve().parent
    start_time = datetime.datetime.now()

    print("=" * 70)
    print("  WMS2.0 AI 增强测试 - 详细日志捕获模式")
    print(f"  开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 清理旧审计日志
    audit_path = project_root / "artifacts" / "ai_decisions.jsonl"
    if audit_path.exists():
        audit_path.unlink()

    # 用猴子补丁拦截所有 complete_json 调用
    from ai.provider import OpenAICompatibleProvider

    original_complete_json = OpenAICompatibleProvider.complete_json

    def patched_complete_json(self, task, payload):
        return intercepted_complete_json(original_complete_json, self, task, payload)

    plugin = AITestLogPlugin()

    with patch.object(OpenAICompatibleProvider, "complete_json", patched_complete_json):
        # Phase 1: AI 单元测试（不含 E2E）
        print("\n[Phase 1] 运行 AI 单元测试（23 项）...")
        exit_code_unit = pytest.main([
            "tests/ai/",
            "--ignore=tests/ai/test_e2e_ai_healing.py",
            "-v",
            "--tb=short",
            "-q",
        ], plugins=[plugin])
        print(f"  单元测试退出码: {exit_code_unit}")

        # Phase 2: E2E AI 自愈测试
        print("\n[Phase 2] 运行 E2E AI 自愈测试...")
        exit_code_e2e = pytest.main([
            "tests/ai/test_e2e_ai_healing.py",
            "-v",
            "--tb=long",
            "-s",
        ], plugins=[plugin])
        print(f"  E2E 测试退出码: {exit_code_e2e}")

    # Phase 3: 回归测试
    print("\n[Phase 3] 运行回归测试...")
    exit_code_reg = pytest.main([
        "tests/smoke/",
        "tests/wms/test_login.py",
        "-v",
        "--tb=short",
    ], plugins=[plugin])
    print(f"  回归测试退出码: {exit_code_reg}")

    end_time = datetime.datetime.now()
    total_duration = (end_time - start_time).total_seconds()

    # 读取审计日志
    audit_entries = []
    if audit_path.exists():
        for line in audit_path.read_text(encoding="utf-8").strip().split("\n"):
            if line.strip():
                try:
                    audit_entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    # 生成 Markdown 报告
    report = generate_report(
        start_time, end_time, total_duration,
        AI_CALL_LOG, TEST_RESULTS, audit_entries,
        exit_code_unit, exit_code_e2e, exit_code_reg,
    )

    output_path = Path(r"C:\Users\26582\Desktop\WMS2.0_AI测试详细日志.md")
    output_path.write_text(report, encoding="utf-8")
    print(f"\n{'=' * 70}")
    print(f"  报告已生成: {output_path}")
    print(f"  总耗时: {total_duration:.1f}s")
    print(f"  AI 调用次数: {len(AI_CALL_LOG)}")
    print(f"  审计日志条数: {len(audit_entries)}")
    print(f"{'=' * 70}")


def generate_report(
    start_time, end_time, total_duration,
    ai_calls, test_results, audit_entries,
    exit_unit, exit_e2e, exit_reg,
):
    """生成超详细的 Markdown 测试报告。"""
    passed = sum(1 for t in test_results if t["outcome"] == "passed")
    failed = sum(1 for t in test_results if t["outcome"] == "failed")
    skipped = sum(1 for t in test_results if t["outcome"] == "skipped")

    # 按任务类型分类 AI 调用
    calls_by_task = {}
    for call in ai_calls:
        task = call["task"]
        calls_by_task.setdefault(task, []).append(call)

    lines = []
    w = lines.append

    w("# WMS2.0 AI 增强功能 - 完整测试过程详细日志")
    w("")
    w(f"> 生成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    w(f"> 测试总耗时: {total_duration:.1f} 秒")
    w("")
    w("---")
    w("")

    # ──── 一、测试概况 ────
    w("## 一、测试环境与配置")
    w("")
    w("| 项目 | 值 |")
    w("|------|-----|")
    w(f"| 开始时间 | {start_time.strftime('%Y-%m-%d %H:%M:%S')} |")
    w(f"| 结束时间 | {end_time.strftime('%Y-%m-%d %H:%M:%S')} |")
    w(f"| 总耗时 | {total_duration:.1f}s |")
    w(f"| AI 模式 | `enhanced` |")
    if ai_calls:
        w(f"| AI 模型 | `{ai_calls[0].get('model', 'N/A')}` |")
        w(f"| API 端点 | `{ai_calls[0].get('base_url', 'N/A')}` |")
    w(f"| AI 调用总次数 | {len(ai_calls)} |")
    w(f"| 审计日志条数 | {len(audit_entries)} |")
    w("")

    # ──── 二、测试结果汇总 ────
    w("## 二、测试结果汇总")
    w("")
    w(f"| 状态 | 数量 |")
    w(f"|------|------|")
    w(f"| 通过 (PASSED) | {passed} |")
    w(f"| 失败 (FAILED) | {failed} |")
    w(f"| 跳过 (SKIPPED) | {skipped} |")
    w(f"| **合计** | **{len(test_results)}** |")
    w("")

    unit_status = "PASSED" if exit_unit == 0 else "FAILED"
    e2e_status = "PASSED" if exit_e2e == 0 else "FAILED"
    reg_status = "PASSED" if exit_reg == 0 else "FAILED"
    w(f"- Phase 1 (AI 单元测试): **{unit_status}** (退出码 {exit_unit})")
    w(f"- Phase 2 (E2E AI 自愈): **{e2e_status}** (退出码 {exit_e2e})")
    w(f"- Phase 3 (回归测试): **{reg_status}** (退出码 {exit_reg})")
    w("")

    # ──── 三、每个测试的详细结果 ────
    w("## 三、每个测试用例的详细结果")
    w("")
    w("| # | 测试用例 | 结果 | 耗时 |")
    w("|---|---------|------|------|")
    for i, t in enumerate(test_results, 1):
        outcome_emoji = {"passed": "PASS", "failed": "FAIL", "skipped": "SKIP"}.get(t["outcome"], t["outcome"])
        w(f"| {i} | `{t['nodeid']}` | {outcome_emoji} | {t['duration']}s |")
    w("")

    if failed > 0:
        w("### 失败测试详情")
        w("")
        for t in test_results:
            if t["outcome"] == "failed":
                w(f"#### `{t['nodeid']}`")
                w("")
                w("```")
                w(t["longrepr"][:2000])
                w("```")
                w("")

    # ──── 四、AI 调用全过程（核心章节） ────
    w("## 四、AI 大模型调用全过程（核心详细日志）")
    w("")
    w(f"本次测试共触发了 **{len(ai_calls)} 次** AI 大模型调用。以下逐一记录每次调用的完整过程：")
    w("")

    for i, call in enumerate(ai_calls, 1):
        w(f"### 第 {i} 次 AI 调用")
        w("")
        w(f"| 属性 | 值 |")
        w(f"|------|-----|")
        w(f"| 调用时间 | `{call['timestamp']}` |")
        w(f"| 任务类型 | `{call['task']}` |")
        w(f"| 模型 | `{call.get('model', 'N/A')}` |")
        w(f"| 耗时 | `{call.get('elapsed_seconds', 'N/A')}s` |")
        w(f"| 调用成功 | `{call.get('success', 'N/A')}` |")
        w("")

        w("**System Prompt (系统提示词):**")
        w("")
        w("```")
        w(call.get("system_prompt", "N/A"))
        w("```")
        w("")

        w("**发送给 AI 的 Payload (输入数据):**")
        w("")
        w("```json")
        try:
            payload_str = json.dumps(call.get("payload_full", {}), ensure_ascii=False, indent=2)
            # 限制长度以避免超长 DOM
            if len(payload_str) > 3000:
                payload_str = payload_str[:3000] + "\n... (已截断，原始长度: " + str(len(payload_str)) + " 字符)"
            w(payload_str)
        except Exception:
            w(str(call.get("payload_summary", {})))
        w("```")
        w("")

        w("**AI 返回结果:**")
        w("")
        if call.get("success"):
            w("```json")
            try:
                w(json.dumps(call.get("response_content", {}), ensure_ascii=False, indent=2))
            except Exception:
                w(str(call.get("response_content", {})))
            w("```")
        else:
            w(f"调用失败，错误信息: `{call.get('error', 'N/A')}`")
        w("")

        if call.get("raw_text"):
            w("**AI 原始返回文本:**")
            w("")
            w("```")
            w(call["raw_text"][:1500])
            w("```")
            w("")

        # 解释 AI 在这次调用中扮演的角色
        task = call["task"]
        if task == "heal_locator":
            w("**AI 角色解析:** AI 作为 **定位器自愈专家**，接收了失败的 CSS 选择器候选和页面 DOM 片段，"
              "分析 DOM 结构后推断出最可靠的 CSS 选择器。这使得当原始定位器因页面结构变更而失效时，"
              "AI 能自动推断出新的有效选择器，无需人工修改测试代码。")
        elif task == "assertion_assistant":
            w("**AI 角色解析:** AI 作为 **智能断言助手**，根据业务流名称、期望条件和页面 HTML 内容，"
              "给出了具体可执行的断言建议（包括要检查什么、用什么选择器、期望值是什么），"
              "帮助测试工程师快速构建精准的页面验证逻辑。")
        elif task == "failure_analysis":
            w("**AI 角色解析:** AI 作为 **失败诊断专家**，接收了失败步骤名、异常信息和页面快照，"
              "自动分析出可能的根因、给出可操作的修复建议，并对问题进行分类"
              "（timeout/ui_failure/network_error/data_mismatch/unknown），"
              "大幅减少了排查问题所需的时间。")
        w("")
        w("---")
        w("")

    # ──── 五、按功能模块的 AI 角色分析 ────
    w("## 五、AI 在各功能模块中的角色与作用详解")
    w("")

    w("### 5.1 AI 定位器自愈 (SelfHealingLocator)")
    w("")
    w("**工作机制:**")
    w("")
    w("```")
    w("1. [规则阶段] 依次尝试候选 CSS 选择器，在真实页面上执行 page.locator(selector).count()")
    w("2. [判断分支] 如果某个候选命中 (count > 0)，直接返回，不进入 AI 阶段")
    w("3. [AI 阶段]  如果所有候选均失败且 AI 模式为 enhanced：")
    w("   a. 提取页面 DOM 片段（最多 8000 字符）")
    w("   b. 将失败候选 + DOM 片段 + 上下文描述发送给 GLM-4.7")
    w("   c. AI 分析 DOM 结构，推断最可靠的 CSS 选择器")
    w("   d. 用 AI 返回的选择器在真实页面上二次校验")
    w("4. [审计记录] 无论走哪条路径，都将决策轨迹写入 JSONL 审计日志")
    w("```")
    w("")

    heal_calls = calls_by_task.get("heal_locator", [])
    w(f"本次测试中 AI 定位器自愈共被调用 **{len(heal_calls)} 次**：")
    w("")
    for i, call in enumerate(heal_calls, 1):
        selector = call.get("response_content", {}).get("selector", "N/A") if call.get("success") else "调用失败"
        w(f"- 第 {i} 次: 任务上下文=`{call.get('payload_full', {}).get('context', 'N/A')}`，"
          f"AI 返回选择器=`{selector}`，耗时={call.get('elapsed_seconds', 'N/A')}s")
    w("")

    w("### 5.2 AI 失败分析代理 (FailureAnalysisAgent)")
    w("")
    w("**工作机制:**")
    w("")
    w("```")
    w("1. [快照采集] 如果 page 对象存在，截取当前页面 HTML 内容（最多 8000 字符）")
    w("2. [判断分支]")
    w("   - AI 模式 disabled 或 provider 不可用: 走本地规则兜底")
    w("     - 包含 'Timeout' → classification='timeout'")
    w("     - 其他异常 → classification='ui_failure'")
    w("   - AI 模式 enhanced 且 provider 可用: 走 AI 诊断路径")
    w("3. [AI 诊断] 将步骤名、异常信息、上下文、页面快照发送给 GLM-4.7")
    w("4. [结构化输出] AI 返回: probable_cause(根因)、suggestion(建议)、classification(分类)")
    w("5. [审计记录] 将分析结果和决策轨迹写入审计日志")
    w("```")
    w("")

    fa_calls = calls_by_task.get("failure_analysis", [])
    w(f"本次测试中 AI 失败分析共被调用 **{len(fa_calls)} 次**：")
    w("")
    for i, call in enumerate(fa_calls, 1):
        content = call.get("response_content", {}) if call.get("success") else {}
        cause = content.get("probable_cause", "N/A")
        classification = content.get("classification", "N/A")
        w(f"- 第 {i} 次: 步骤=`{call.get('payload_full', {}).get('step_name', 'N/A')}`，"
          f"分类=`{classification}`，根因=`{cause[:80]}`，耗时={call.get('elapsed_seconds', 'N/A')}s")
    w("")

    w("### 5.3 AI 断言助手 (AssertionAssistant)")
    w("")
    w("**工作机制:**")
    w("")
    w("```")
    w("1. [前置检查] AI 模式是否 disabled / provider 是否存在且可用")
    w("2. [数据组装] 将业务流名称、期望条件、页面 HTML 摘要发送给 GLM-4.7")
    w("3. [AI 建议] AI 返回结构化断言建议:")
    w('   - assertions: [{"check": "...", "selector": "...", "expected": "..."}]')
    w("   - confidence: 0.0-1.0 的置信度分数")
    w("   - reasoning: AI 的推理过程说明")
    w("4. [降级处理] 如果 AI 不可用，返回 {enabled: false} 元数据")
    w("```")
    w("")

    aa_calls = calls_by_task.get("assertion_assistant", [])
    w(f"本次测试中 AI 断言助手共被调用 **{len(aa_calls)} 次**：")
    w("")
    for i, call in enumerate(aa_calls, 1):
        content = call.get("response_content", {}) if call.get("success") else {}
        confidence = content.get("confidence", "N/A")
        assertions = content.get("assertions", [])
        w(f"- 第 {i} 次: 业务流=`{call.get('payload_full', {}).get('flow_name', 'N/A')}`，"
          f"置信度=`{confidence}`，断言建议数=`{len(assertions)}`，耗时={call.get('elapsed_seconds', 'N/A')}s")
    w("")

    w("### 5.4 AI Provider 通信层 (OpenAICompatibleProvider)")
    w("")
    w("**工作机制:**")
    w("")
    w("```")
    w("1. [可用性检查] 验证 base_url、api_key、model 均非空")
    w("2. [提示词选择] 根据 task 名称从 TASK_PROMPTS 字典中选择专用 system prompt")
    w("3. [请求构造] 组装 OpenAI 兼容格式的 chat/completions 请求体")
    w("   - model: glm-4.7")
    w("   - temperature: 0.1 (低温度 = 高确定性)")
    w("   - response_format: json_object (强制 JSON 输出)")
    w("4. [重试机制] 使用 tenacity 指数退避重试:")
    w("   - 最大重试次数: 5 (由 AI_MAX_RETRIES 配置)")
    w("   - 等待策略: wait_exponential(multiplier=2, min=2s, max=30s)")
    w("   - 重试间隔: 2s → 4s → 8s → 16s → 30s")
    w("5. [响应解析] 提取 choices[0].message.content 并 JSON 解析")
    w("6. [审计日志] 以 JSONL 格式追加到 artifacts/ai_decisions.jsonl")
    w("```")
    w("")

    # ──── 六、审计日志详情 ────
    w("## 六、AI 决策审计日志 (JSONL)")
    w("")
    w(f"审计日志共 **{len(audit_entries)}** 条记录：")
    w("")
    for i, entry in enumerate(audit_entries, 1):
        w(f"### 审计记录 #{i}")
        w("")
        w("```json")
        w(json.dumps(entry, ensure_ascii=False, indent=2))
        w("```")
        w("")

    # ──── 七、AI 对测试流程的整体影响 ────
    w("## 七、AI 对测试流程的整体影响与价值总结")
    w("")
    w("### 7.1 AI 的三大核心能力")
    w("")
    w("| 能力 | 作用 | 触发条件 | 本次调用次数 |")
    w("|------|------|---------|------------|")
    w(f"| **定位器自愈** | 当 CSS 选择器失效时，AI 分析 DOM 推断新选择器 | "
      f"所有候选选择器在页面上 count=0 | {len(heal_calls)} |")
    w(f"| **失败诊断** | 测试失败时 AI 分析根因，给出修复建议和分类 | "
      f"测试步骤抛出异常 | {len(fa_calls)} |")
    w(f"| **断言建议** | AI 根据页面内容推荐精准的断言验证点 | "
      f"需要验证复杂页面状态 | {len(aa_calls)} |")
    w("")

    w("### 7.2 传统自动化 vs AI 增强自动化对比")
    w("")
    w("| 场景 | 传统方式 | AI 增强方式 |")
    w("|------|---------|-----------|")
    w("| 页面结构变更导致选择器失效 | 测试失败，人工修改选择器 | AI 自动分析 DOM，推断新选择器并验证 |")
    w("| 测试失败排查 | 查看截图和日志，人工分析 | AI 自动诊断根因，给出分类和修复建议 |")
    w("| 编写断言验证 | 人工检查页面，手写断言代码 | AI 分析页面内容，推荐具体断言点和期望值 |")
    w("| 测试维护成本 | 高（频繁手动更新） | 低（AI 自动适应变化） |")
    w("")

    w("### 7.3 AI 决策链路完整流程图")
    w("")
    w("```")
    w("测试用例执行")
    w("    │")
    w("    ├── 定位元素 ──→ SelfHealingLocator.resolve()")
    w("    │       │")
    w("    │       ├── [规则阶段] 尝试候选 selector")
    w("    │       │       ├── 命中 → 返回 source='rule' ✓")
    w("    │       │       └── 全部失败 → 进入 AI 阶段")
    w("    │       │")
    w("    │       └── [AI 阶段] GLM-4.7 分析 DOM")
    w("    │               ├── 提取 DOM 片段 + 候选列表")
    w("    │               ├── 调用 complete_json('heal_locator', payload)")
    w("    │               ├── AI 返回推断的 selector")
    w("    │               ├── 二次校验: page.locator(selector).count() > 0")
    w("    │               └── 返回 source='ai', success=True/False")
    w("    │")
    w("    ├── 验证结果 ──→ AssertionAssistant.suggest()")
    w("    │       ├── 组装 flow_name + expectations + page_summary")
    w("    │       ├── 调用 complete_json('assertion_assistant', payload)")
    w("    │       └── AI 返回断言建议 {assertions, confidence, reasoning}")
    w("    │")
    w("    └── 失败分析 ──→ FailureAnalysisAgent.analyze()")
    w("            ├── 截取页面快照")
    w("            ├── 调用 complete_json('failure_analysis', payload)")
    w("            └── AI 返回 {probable_cause, suggestion, classification}")
    w("```")
    w("")

    # ──── 八、AI 调用统计 ────
    w("## 八、AI 调用性能统计")
    w("")
    if ai_calls:
        success_calls = [c for c in ai_calls if c.get("success")]
        failed_calls = [c for c in ai_calls if not c.get("success")]
        avg_time = sum(c.get("elapsed_seconds", 0) for c in ai_calls) / len(ai_calls)
        max_time = max(c.get("elapsed_seconds", 0) for c in ai_calls)
        min_time = min(c.get("elapsed_seconds", 0) for c in ai_calls)

        w(f"| 指标 | 值 |")
        w(f"|------|-----|")
        w(f"| 总调用次数 | {len(ai_calls)} |")
        w(f"| 成功次数 | {len(success_calls)} |")
        w(f"| 失败次数 | {len(failed_calls)} |")
        w(f"| 平均响应时间 | {avg_time:.3f}s |")
        w(f"| 最快响应 | {min_time:.3f}s |")
        w(f"| 最慢响应 | {max_time:.3f}s |")
        w(f"| 成功率 | {len(success_calls)/len(ai_calls)*100:.1f}% |")
    else:
        w("本次运行未触发任何 AI 调用。")
    w("")

    w("---")
    w("")
    w(f"*报告生成完毕 - {end_time.strftime('%Y-%m-%d %H:%M:%S')}*")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
