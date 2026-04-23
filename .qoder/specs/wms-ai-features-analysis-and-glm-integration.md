# WMS2.0 AI特色功能分析、GLM集成与全面测试

## Context

WMS2.0项目内置了一套完整的AI增强UI自动化框架（`src/ai/`），包含自愈定位、智能断言、失败分析、审计追踪四大能力。但当前 **AI功能处于未激活状态**（`.env` 中 `AI_MODE=disabled`，API凭证为占位符），且存在若干代码Bug和设计短板。用户需要：

1. 对AI功能进行全面技术评估
2. 修复已发现的Bug和不足
3. 接入智谱GLM-4.7大模型API使AI功能真正可用
4. 编写全面的测试用例验证所有AI能力

---

## Part 1: AI功能清单与技术评估

### AI模块架构总览

```
src/ai/
  provider.py          ← OpenAI兼容Provider（HTTP客户端 + 重试 + 审计）
  locator.py           ← 自愈定位器（规则优先 → AI推断 → 二次校验）
  assertion.py         ← 断言助手（页面语义断言建议）
  failure_analysis.py  ← 失败分析代理（AI诊断 + 本地兜底分类）
  report_enricher.py   ← 报告增强器（JSON序列化）
  models.py            ← 数据模型（AIResponse, DecisionTrace等）
```

### 逐模块评估

| 模块 | 质量 | 架构 | 可维护性 | 关键问题 |
|------|------|------|----------|----------|
| provider.py | 7/10 | 6/10 | 6/10 | 提示词过于泛化；max_retries配置未生效 |
| locator.py | 7/10 | 7/10 | 5/10 | candidates迭代器二次消耗Bug |
| assertion.py | 7/10 | 5/10 | 6/10 | 从未被实际调用 |
| failure_analysis.py | 8/10 | 6/10 | 7/10 | 从未被实际调用 |
| report_enricher.py | 5/10 | 3/10 | 4/10 | 无AI逻辑，仅JSON序列化 |
| models.py | 8/10 | 8/10 | 8/10 | 设计良好 |

### 已发现问题清单

| 编号 | 类型 | 严重度 | 描述 | 文件:行号 |
|------|------|--------|------|-----------|
| BUG-1 | Bug | 高 | `max_retries`配置未生效：tenacity装饰器硬编码`stop_after_attempt(2)`，忽略`AISettings.max_retries` | provider.py:38 |
| BUG-2 | Bug | 中 | `candidates`迭代器消耗：`resolve()`中`Iterable`被第一次for循环消耗，AI阶段再遍历时为空（generator场景） | locator.py:33,62 |
| DSG-1 | 设计 | 高 | 系统提示词过于泛化：三种不同AI任务共用一句话提示词，模型缺乏任务特定指导 | provider.py:65 |
| DSG-2 | 设计 | 中 | `AssertionAssistant.suggest()`从未被任何Flow或测试调用 | assertion.py |
| DSG-3 | 设计 | 中 | `FailureAnalysisAgent.analyze()`从未被任何Flow或测试调用 | failure_analysis.py |
| DSG-4 | 设计 | 低 | `ReportEnricher`仅做JSON写入，无AI增强逻辑 | report_enricher.py |
| TST-1 | 测试 | 高 | 无任何AI模块的单元测试 | tests/ |

---

## Part 2: Bug修复与改进

### 2.1 修复 candidates 迭代器消耗Bug

**文件**: `src/ai/locator.py`
**改动**: 在`resolve()`方法入口将`Iterable`物化为`list`

```python
# 第32行，方法体第一行添加：
candidates = list(candidates)
```

签名类型`Iterable[LocatorCandidate]`保持不变（list也是Iterable），仅内部确保两次遍历都基于同一列表。

### 2.2 修复 max_retries 配置未生效

**文件**: `src/ai/provider.py`
**改动**: 移除静态`@retry`装饰器，改为在`__init__`中动态创建带重试的请求方法

```python
# 移除第38行的 @retry 装饰器
# 在 __init__ 中动态装饰：
def __init__(self, settings: AISettings) -> None:
    self.settings = settings
    self.session = requests.Session()
    self._do_request = retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_fixed(1),
        reraise=True,
    )(self._do_request)

# 将原 _request 方法重命名为 _do_request（不带装饰器）
def _do_request(self, body: dict[str, Any]) -> requests.Response:
    # ...原实现不变...

# _request 调用 _do_request
def _request(self, body):
    return self._do_request(body)
```

### 2.3 添加任务专用提示词系统

**文件**: `src/ai/provider.py`
**改动**: 在类中新增`TASK_PROMPTS`字典，`complete_json()`根据task参数选择提示词

```python
TASK_PROMPTS = {
    "heal_locator": (
        "你是一个Web UI自动化测试的定位器自愈专家。\n"
        "你将收到一组失败的CSS候选定位器、页面DOM片段和上下文描述。\n"
        "请分析DOM结构，推断目标元素最可靠的CSS选择器。\n"
        "优先使用id、data-testid、aria属性，避免脆弱的层级路径。\n"
        "严格返回JSON格式: {\"selector\": \"<有效的CSS选择器>\"}"
    ),
    "assertion_assistant": (
        "你是一个UI自动化测试的智能断言助手。\n"
        "你将收到业务流名称、期望条件和页面HTML摘要。\n"
        "请根据页面实际内容，给出具体可执行的断言建议。\n"
        "返回JSON格式: {\"assertions\": [{\"check\": \"描述\", \"selector\": \"...\", \"expected\": \"...\"}], \"confidence\": 0.0-1.0, \"reasoning\": \"...\"}"
    ),
    "failure_analysis": (
        "你是一个UI自动化测试失败诊断专家。\n"
        "你将收到失败步骤名、异常信息、额外上下文和页面快照。\n"
        "请分析根因并给出具体可操作的修复建议。\n"
        "classification必须为以下之一: timeout, ui_failure, network_error, data_mismatch, unknown\n"
        "返回JSON格式: {\"probable_cause\": \"...\", \"suggestion\": \"...\", \"classification\": \"...\"}"
    ),
}
DEFAULT_PROMPT = "你是一个 UI 自动化智能助手。请输出 JSON，并保持结果可解释。"
```

在`complete_json()`中将第65行替换为：
```python
"content": self.TASK_PROMPTS.get(task, self.DEFAULT_PROMPT),
```

---

## Part 3: GLM-4.7 API集成

### 3.1 更新 `.env` 配置

**文件**: `.env`

```env
AI_MODE=enhanced
AI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
AI_API_KEY=35404fc352624732bb855e0e408da4a0.zTAVl6xDC6PSuByF
AI_MODEL=glm-4.7
AI_TIMEOUT_SECONDS=30
AI_MAX_RETRIES=2
```

### 3.2 兼容性确认

项目的`OpenAICompatibleProvider`与GLM-4.7 API**完全兼容**，无需修改Provider代码：

| 检查项 | 项目代码 | GLM兼容性 |
|--------|---------|-----------|
| 端点 | `{base_url}/chat/completions` | GLM使用相同路径 |
| 认证 | `Authorization: Bearer {key}` | GLM使用相同格式 |
| response_format | `{"type": "json_object"}` | GLM-4.7支持 |
| temperature | 0.1 | GLM支持0-1范围 |

---

## Part 4: AI功能单元测试

### 4.1 注册pytest marker

**文件**: `pyproject.toml`
在`markers`列表中添加：
```
"ai: AI module tests (may call external API)"
```

### 4.2 测试目录结构

```
tests/ai/
  __init__.py
  conftest.py              ← AI测试专用fixtures
  test_provider.py         ← Provider连通性+核心逻辑 (4个用例)
  test_locator.py          ← SelfHealingLocator逻辑 (5个用例)
  test_assertion.py        ← AssertionAssistant调用 (3个用例)
  test_failure_analysis.py ← FailureAnalysisAgent逻辑 (5个用例)
  test_audit_log.py        ← 审计日志写入 (3个用例)
  test_config_loading.py   ← AI配置加载 (3个用例)
  test_e2e_ai_healing.py   ← E2E AI自愈测试 (1个用例)
```

### 4.3 tests/ai/conftest.py 核心fixtures

```python
# ai_settings: 从项目配置加载真实AISettings (mode=enhanced, GLM配置)
# disabled_ai_settings: mode=disabled的AISettings
# real_provider: 基于ai_settings创建真实OpenAICompatibleProvider
# mock_page: MagicMock(spec=Page), 可控的locator().count()返回值
# tmp_audit_path: 临时审计日志路径
```

### 4.4 测试用例清单

#### test_provider.py (4个用例)
| 用例 | 标记 | 验证内容 |
|------|------|----------|
| `test_glm_api_connectivity` | @ai | 调用GLM API，断言response.success=True，content非空 |
| `test_provider_not_configured` | @ai | base_url为空时返回success=False |
| `test_provider_is_available_check` | @ai | 缺url/key/model三种场景都返回False |
| `test_provider_json_response_format` | @ai | 验证GLM返回可JSON序列化的结构化内容 |

#### test_locator.py (5个用例)
| 用例 | 标记 | 验证内容 |
|------|------|----------|
| `test_rule_based_match_succeeds` | @ai | mock page命中规则，返回source="rule" |
| `test_rule_fails_ai_disabled` | @ai | 规则失败+AI禁用，返回success=False |
| `test_candidates_not_exhausted` | @ai | **验证BUG-2修复**: generator候选在AI阶段仍可用 |
| `test_ai_heals_with_valid_selector` | @ai | mock provider返回有效selector，二次校验通过 |
| `test_ai_selector_fails_verification` | @ai | AI返回selector但二次校验失败 |

#### test_assertion.py (3个用例)
| 用例 | 标记 | 验证内容 |
|------|------|----------|
| `test_disabled_returns_meta` | @ai | disabled模式返回`{"enabled": False}` |
| `test_with_real_glm` | @ai | 真实GLM调用，返回非空建议 |
| `test_provider_none` | @ai | provider=None返回disabled |

#### test_failure_analysis.py (5个用例)
| 用例 | 标记 | 验证内容 |
|------|------|----------|
| `test_local_fallback_timeout` | @ai | Timeout异常→classification="timeout" |
| `test_local_fallback_ui_failure` | @ai | 其他异常→classification="ui_failure" |
| `test_ai_path_with_real_glm` | @ai | 真实GLM诊断，返回有意义的cause/suggestion |
| `test_page_none_handled` | @ai | page=None不抛异常 |
| `test_page_content_exception` | @ai | page.content()抛异常时优雅降级 |

#### test_audit_log.py (3个用例)
| 用例 | 标记 | 验证内容 |
|------|------|----------|
| `test_creates_file_and_appends` | @ai | 两次append后文件有两行合法JSON |
| `test_directory_auto_created` | @ai | 深层路径自动创建 |
| `test_locator_writes_audit` | @ai | resolve()后审计文件有对应记录 |

#### test_config_loading.py (3个用例)
| 用例 | 标记 | 验证内容 |
|------|------|----------|
| `test_default_ai_settings` | @ai | 默认值: mode=enhanced, max_retries=2 |
| `test_env_overrides_yaml` | @ai | 环境变量AI_MODE=disabled覆盖YAML |
| `test_max_retries_from_env` | @ai | AI_MAX_RETRIES=5能被正确加载 |

### 4.5 E2E AI自愈测试

**文件**: `tests/ai/test_e2e_ai_healing.py`
**标记**: `@pytest.mark.ai`, `@pytest.mark.e2e`

```
测试流程:
1. require_live_ui + AI可用性检查（不满足则skip）
2. 打开WMS登录页（http://test.wms-v2.eccang.com/auth/login）
3. 构造故意错误的候选定位器:
   - LocatorCandidate("wrong-id", "#nonexistent_username")
   - LocatorCandidate("wrong-class", ".wrong-class-name")
4. 调用 SelfHealingLocator.resolve(page, wrong_candidates, "WMS登录用户名输入框")
5. 验证:
   - resolution.source == "ai" (确认走了AI路径)
   - resolution.success == True (AI推断的selector通过二次校验)
   - page.locator(resolution.selector).count() > 0
```

---

## Part 5: 实施顺序

```
Phase 1: 基础修复（无外部依赖）
  1a. locator.py — 修复candidates迭代器消耗 (1行)
  1b. provider.py — 修复max_retries硬编码 (~10行)
  1c. pyproject.toml — 注册 "ai" pytest marker (1行)

Phase 2: 提示词增强（依赖1b）
  2a. provider.py — 添加TASK_PROMPTS字典 + complete_json()选择逻辑 (~30行)

Phase 3: GLM配置接入（独立）
  3a. .env — 更新AI配置为GLM-4.7真实值 (6行)

Phase 4: 单元测试（依赖1+2+3）
  4a. 创建 tests/ai/ 目录和conftest.py
  4b. 编写6个测试文件（24个用例）
  4c. 运行验证

Phase 5: E2E测试（依赖全部）
  5a. 编写 test_e2e_ai_healing.py
  5b. 运行验证
```

---

## 关键文件清单

| 文件 | 操作 | 改动量 |
|------|------|--------|
| `src/ai/provider.py` | 修改 | ~50行（max_retries修复 + 提示词系统） |
| `src/ai/locator.py` | 修改 | 1行（candidates物化） |
| `.env` | 修改 | 6行（GLM配置） |
| `pyproject.toml` | 修改 | 1行（ai marker） |
| `tests/ai/__init__.py` | 新建 | 空 |
| `tests/ai/conftest.py` | 新建 | ~60行 |
| `tests/ai/test_provider.py` | 新建 | ~80行 |
| `tests/ai/test_locator.py` | 新建 | ~120行 |
| `tests/ai/test_assertion.py` | 新建 | ~50行 |
| `tests/ai/test_failure_analysis.py` | 新建 | ~100行 |
| `tests/ai/test_audit_log.py` | 新建 | ~60行 |
| `tests/ai/test_config_loading.py` | 新建 | ~50行 |
| `tests/ai/test_e2e_ai_healing.py` | 新建 | ~50行 |

---

## 验证方案

```batch
REM 1. 运行AI单元测试（不需要浏览器）
.venv\Scripts\pytest.exe tests/ai/ -m "ai and not e2e" -v

REM 2. 运行E2E AI自愈测试（需要浏览器 + GLM API）
.venv\Scripts\pytest.exe tests/ai/test_e2e_ai_healing.py -v -s

REM 3. 回归验证：确保现有测试不受影响
.venv\Scripts\pytest.exe tests/smoke/ -v
.venv\Scripts\pytest.exe tests/wms/test_login.py -v -s
```

## 向后兼容保证

所有改动在`AI_MODE=disabled`时**行为完全不变**：
- 提示词映射：不会被触发（complete_json不调用）
- max_retries修复：不会被触发（_request不调用）
- candidates修复：纯数据操作，不涉及AI
- 新测试文件：独立目录，不影响现有测试
- .env配置：AI_MODE行仍可改回disabled
