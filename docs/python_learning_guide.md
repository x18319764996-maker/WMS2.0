# 🐍 通过 WMS2.0 项目学 Python — 从零到跑通

> **学习理念**：不讲空洞语法，只通过项目中的真实代码来理解 Python。每一节都从你眼前的文件出发。

---

## 📖 目录

1. [第一章：这个项目是怎么跑起来的](#第一章这个项目是怎么跑起来的)
2. [第二章：Python 基础语法 — 在项目中认出它们](#第二章python-基础语法--在项目中认出它们)
3. [第三章：面向对象 — 项目架构的骨架](#第三章面向对象--项目架构的骨架)
4. [第四章：函数进阶 — 装饰器、生成器与上下文管理器](#第四章函数进阶--装饰器生成器与上下文管理器)
5. [第五章：类型系统与数据模型](#第五章类型系统与数据模型)
6. [第六章：异常处理与容错机制](#第六章异常处理与容错机制)
7. [第七章：pytest 测试框架深度解析](#第七章pytest-测试框架深度解析)
8. [第八章：AI 模块 — 把所有知识串起来](#第八章ai-模块--把所有知识串起来)

---

## 第一章：这个项目是怎么跑起来的

### 1.1 一条命令的旅程

当你在终端输入 `python main.py run wms` 时，发生了什么？我们一步步追踪：

```
你敲的命令: python main.py run wms
        ↓
main.py 的 if __name__ == "__main__" 被触发
        ↓
build_parser() 解析命令行参数 → args.command = "run", args.target = "wms"
        ↓
cmd_run(["wms"]) 被调用
        ↓
委托给 utils/run_all_scenarios.py 的 main()
        ↓
组装 pytest 命令行 → subprocess.call() 执行
        ↓
pytest 发现 tests/wms/ 下的测试文件
        ↓
conftest.py 的 fixture 自动注入依赖（浏览器、配置、页面对象…）
        ↓
测试函数执行 → 页面对象操作浏览器 → 断言结果
```

### 1.2 入口文件 main.py 逐行解读

打开 `main.py`，我们来逐块理解：

```python
"""WMS+OMS AI UI 自动化框架主入口。

提供统一的 CLI 命令：
    python main.py run [target]     运行测试场景
    python main.py check            检查运行环境
    python main.py report           打开最新测试报告
"""
```

🔑 **知识点：三引号字符串（docstring）**
- 用 `"""..."""` 包裹的是文档字符串，放在文件/函数/类的开头，Python 会自动把它赋给 `__doc__` 属性
- 这是 Python 的"自文档化"文化——代码即文档

```python
from __future__ import annotations
```

🔑 **知识点：from __future__ import annotations**
- 这行启用了"延迟注解求值"，让你可以写 `list[str]` 而不用写 `List[str]`（Python 3.9 以下需要）
- 项目中到处可见，是现代 Python 项目的标配

```python
import argparse
import os
import sys
import webbrowser
from pathlib import Path
```

🔑 **知识点：import 导入模块**
- `import X` — 把整个模块 X 拿进来，用 `X.功能` 调用
- `from X import Y` — 只拿模块 X 中的 Y，直接用 `Y` 调用
- Python 标准库非常丰富，上面这些分别是：
  - `argparse`：命令行参数解析
  - `os`：操作系统接口（环境变量、路径等）
  - `sys`：Python 解释器相关（路径、退出等）
  - `webbrowser`：打开浏览器
  - `pathlib.Path`：面向对象的路径操作（比 `os.path` 更优雅）

```python
project_root = Path(__file__).resolve().parent
src_path = str(project_root / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
```

🔑 **知识点：路径操作与 sys.path**
- `__file__`：当前 Python 文件的路径
- `.resolve()`：转为绝对路径（解析所有符号链接）
- `.parent`：取父目录
- `/` 运算符：Path 对象重载了 `/`，可以用 `Path("a") / "b"` 代替 `os.path.join("a", "b")`
- `sys.path`：Python 的模块搜索路径列表，`insert(0, ...)` 把 src 目录加到最前面，确保能 import 到项目源码

```python
def cmd_check() -> int:
    """检查项目运行所需的最小环境。"""
    issues = 0
    project_root = Path(__file__).resolve().parent

    env_file = project_root / ".env"
    if env_file.exists():
        print("[OK] .env 文件已存在")
    else:
        print("[WARN] .env 文件不存在，将使用 config/*.yaml 中的默认值")
        issues += 1
```

🔑 **知识点：函数定义、返回值类型、条件判断**
- `def cmd_check() -> int:`：`-> int` 是返回值类型注解（不影响运行，但帮助人类理解）
- `issues = 0`：Python 不需要声明变量类型，直接赋值即可
- `if ... else ...`：缩进代替大括号，这是 Python 最鲜明的特征
- `issues += 1`：等同于 `issues = issues + 1`

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

🔑 **知识点：Python 的入口守卫**
- `__name__`：当文件被直接运行时为 `"__main__"`，被 import 时为模块名
- 这是 Python 的经典模式：文件既能被直接运行，也能被其他文件 import
- `raise SystemExit(code)`：以指定退出码结束程序（0=成功，非0=失败）

### 1.3 运行编排器 run_all_scenarios.py

```python
command = [
    sys.executable,        # 当前 Python 解释器的路径
    "-m",                  # 以模块方式运行
    "pytest",              # 运行 pytest 模块
    "--html=artifacts/reports/pytest-report.html",
    "--self-contained-html",
]
```

🔑 **知识点：列表与 subprocess**
- `[...]`：Python 列表（list），有序可变序列
- `sys.executable`：当前 Python 解释器的绝对路径，确保用同一个 Python 运行 pytest
- `subprocess.call(command)`：在子进程中执行命令，等待完成后返回退出码

```python
target_map = {
    "all": [],
    "oms": ["tests/oms"],
    "wms": ["tests/wms"],
    "cross_system": ["tests/cross_system"],
    "smoke": ["tests/smoke"],
}
return target_map.get(target, [target])
```

🔑 **知识点：字典与 .get() 方法**
- `{key: value}`：Python 字典（dict），键值对映射
- `.get(key, default)`：安全取值，键不存在时返回 default 而不是报错
- 这是"优雅降级"的写法——不认识的目标名直接当路径传入

### 1.4 配置加载的三层体系

```python
# ConfigLoader.load() 方法中
load_dotenv(self.project_root / ".env", override=False)    # 第1层：.env 文件
config_path = self.config_dir / f"{target_env}.yaml"        # 第2层：YAML 文件
raw["execution"] = self._apply_execution_overrides(...)      # 第3层：环境变量覆盖
return AppConfig.model_validate(raw)                         # Pydantic 校验
```

🔑 **知识点：f-string 格式化字符串**
- `f"{target_env}.yaml"`：f 开头的字符串中 `{}` 内的表达式会被求值替换
- 这是 Python 3.6+ 引入的，比 `%s` 和 `.format()` 都更直观

🔑 **知识点：三层配置的优先级**
1. `.env` 文件 — 本地开发配置（不提交到 Git）
2. `config/test.yaml` — 环境的默认配置
3. 环境变量 — CI/CD 或命令行覆盖（最高优先级）

这种模式在企业级项目中非常常见，理解它你就理解了"配置即代码"的思想。

---

## 第二章：Python 基础语法 — 在项目中认出它们

### 2.1 变量与数据类型

项目中的真实例子：

```python
# src/core/config/models.py
browser: str = "chromium"           # 字符串
headless: bool = False              # 布尔值
slow_mo: int = 0                    # 整数
default_timeout_ms: int = 10_000    # 整数（下划线分隔，更易读）
timeout_seconds: float = 20.0       # 浮点数

# 字典
oms_endpoints: Dict[str, str] = Field(default_factory=dict)

# 列表
command = [sys.executable, "-m", "pytest"]

# Path 对象
artifact_root: Path = Path("artifacts")
```

🔑 **知识点：Python 的数字下划线**
- `10_000` 等于 `10000`，下划线只是视觉分隔，Python 3.6+ 支持
- 在大数字中特别有用：`1_000_000` 比 `1000000` 易读得多

### 2.2 字符串操作

```python
# f-string（最常用）
f"{self.settings.base_url.rstrip('/')}/chat/completions"
# 解读：先去掉末尾的 /，再拼接路径

# 多行字符串（用于 AI 提示词）
TASK_PROMPTS = {
    "heal_locator": (
        "你是一个Web UI自动化测试的定位器自愈专家。\n"
        "你将收到一组失败的CSS候选定位器、页面DOM片段和上下文描述。\n"
        '严格返回JSON格式: {"selector": "<有效的CSS选择器>"}'
    ),
}
```

🔑 **知识点：字符串拼接技巧**
- 括号内多个字符串字面量会自动拼接：`("a" "b")` → `"ab"`
- `\n`：换行符
- `.rstrip('/')`：去掉字符串右端的 `/`

### 2.3 条件与循环

```python
# if-elif-else（run_all_scenarios.py）
if args.target != "smoke":
    command.extend(["-m", "e2e"])
if args.keyword:
    command.extend(["-k", args.keyword])

# for 循环（main.py cmd_check）
for browser in browsers:
    try:
        getattr(p, browser).launch()
        print(f"[OK] Playwright {browser} 浏览器可用")
    except Exception:
        print(f"[WARN] Playwright {browser} 未安装")

# for 循环 + 枚举（ai/locator.py）
for candidate in candidates:
    if self._matches(page, candidate.selector):
        return LocatorResolution(candidate.selector, "rule", True, trace)
```

🔑 **知识点：try-except 异常捕获**
- `try` 块中的代码如果出错，不会崩溃，而是跳到 `except` 块
- `Exception` 是所有异常的基类，捕获它等于"出了任何错都兜住"
- 项目中大量使用，这是"容错编程"的基础

### 2.4 列表推导式与生成器

```python
# 项目中没有直接使用，但理解这个模式很重要：

# 列表推导式 — 从一个列表生成新列表
browsers = ["chromium", "firefox", "webkit"]
available = [b for b in browsers if is_installed(b)]
# 等价于：
# available = []
# for b in browsers:
#     if is_installed(b):
#         available.append(b)

# 字典推导式
results = {name: selector for name, selector in candidates}
```

### 2.5 解包与多返回值

```python
# ai/provider.py 中的 JSON 解析
raw = response.json()
message = raw["choices"][0]["message"]["content"]
```

🔑 **知识点：链式取值**
- Python 的字典和列表可以链式访问：`dict["key1"][0]["key2"]`
- 这是处理 API 返回的 JSON 数据时的常见操作

---

## 第三章：面向对象 — 项目架构的骨架

### 3.1 类与继承：最核心的设计模式

这个项目的核心架构就是"继承树"：

```
BasePage（页面对象基类）
├── WMSLoginPage
├── WMSInboundPage
├── WMSInventoryPage
├── WMSOutboundPage
├── OMSLoginPage
└── OMSOrderPage

BaseFlow（业务流基类）
├── WMSWarehouseFlow
├── OMSOrderFlow
└── CrossSystemOrderFulfillmentFlow

LocatorStrategy（定位策略抽象基类）
└── SelfHealingLocator（自愈定位器实现）

AIProvider（AI提供者抽象基类）
└── OpenAICompatibleProvider
```

### 3.2 BasePage — 看懂一个完整的类

```python
class BasePage:
    """页面对象基类，封装自愈定位、导航、点击、填写和断言等通用 UI 操作。"""

    def __init__(self, page: Page, locator_strategy: SelfHealingLocator) -> None:
        """注入 Playwright Page 与自愈定位策略。"""
        self.page = page
        self.locator_strategy = locator_strategy
        self.wait = WaitHelper(page)
```

🔑 **知识点：类的定义**
- `class BasePage:` — 定义一个类
- `__init__` — 构造函数，创建对象时自动调用
- `self` — 指向对象自身，类似 Java 的 `this`
- `self.page = page` — 将参数保存为实例属性

```python
    def smart_locator(self, name: str, candidates: list[LocatorCandidate], context: str) -> Locator:
        """按候选列表依次尝试定位；全部失败时视 AI 配置决定是否调用自愈服务。"""
        resolution = self.locator_strategy.resolve(self.page, candidates, context)
        if not resolution.success:
            raise LookupError(f"页面定位失败: {name} | {context}")
        return self.page.locator(resolution.selector).first
```

🔑 **知识点：方法定义**
- 第一个参数永远是 `self`
- `-> Locator`：返回值类型注解
- 方法可以调用其他方法：`self.locator_strategy.resolve(...)`
- `.first`：属性访问，Playwright Locator 的 `.first` 取第一个匹配元素

### 3.3 继承：子类如何复用和扩展父类

```python
# 父类 BasePage 定义了通用方法
class BasePage:
    def open(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def click(self, name, candidates, context):
        self.smart_locator(name, candidates, context).click()

    def fill(self, name, value, candidates, context):
        locator = self.smart_locator(name, candidates, context)
        locator.fill(value)

# 子类 WMSLoginPage 继承并只写业务特有的方法
class WMSLoginPage(BasePage):
    def open_login(self, base_url: str, login_path: str) -> None:
        self.open(f"{base_url.rstrip('/')}{login_path}")  # 调用父类的 open
        self.page.locator("#username").wait_for(state="visible", timeout=30000)

    def login(self, username: str, password: str) -> None:
        self.fill("wms_username", username, [...], "WMS 登录用户名输入框")  # 调用父类的 fill
        self.fill("wms_password", password, [...], "WMS 登录密码输入框")
        self.click("wms_login", [...], "WMS 登录按钮")  # 调用父类的 click
```

🔑 **知识点：继承的核心价值**
- **复用**：子类不用重写 `open`、`click`、`fill` 等通用方法
- **聚焦**：子类只关心"这个页面有什么特殊操作"
- **一致性**：所有页面对象都有相同的调用方式，降低学习成本

### 3.4 抽象基类（ABC）：定义契约

```python
from abc import ABC, abstractmethod

class AIProvider(ABC):
    """AI 提供者抽象接口。"""

    @abstractmethod
    def complete_json(self, task: str, payload: dict[str, Any]) -> AIResponse:
        """向模型发送任务与上下文，返回结构化 JSON 响应。"""
        raise NotImplementedError

class LocatorStrategy:
    """定位策略抽象基类。"""

    def resolve(self, page, candidates, context) -> LocatorResolution:
        raise NotImplementedError
```

🔑 **知识点：抽象基类**
- `ABC`：Abstract Base Class 的缩写
- `@abstractmethod`：装饰器，标记这个方法必须由子类实现
- 如果子类没有实现抽象方法，Python 会在实例化时抛出 `TypeError`
- 这是一种"契约设计"：父类说"你必须实现这些方法"，子类说"我实现了"

### 3.5 组合优于继承

```python
class WMSWarehouseFlow(BaseFlow):
    def __init__(self, login_page, inbound_page, inventory_page, outbound_page,
                 api_client, assertion_assistant, failure_analysis_agent):
        super().__init__(assertion_assistant, failure_analysis_agent)  # 调用父类 __init__
        self.login_page = login_page          # 组合：持有页面对象
        self.inbound_page = inbound_page       # 组合：持有页面对象
        self.inventory_page = inventory_page   # 组合：持有页面对象
        self.outbound_page = outbound_page     # 组合：持有页面对象
        self.api_client = api_client           # 组合：持有 API 客户端
```

🔑 **知识点：super() 与组合模式**
- `super().__init__(...)`：调用父类的构造函数
- Flow 不继承 Page，而是**持有** Page — 这就是"组合"
- 设计原则："Has-A"（有一个）用组合，"Is-A"（是一个）用继承
- WMSWarehouseFlow **不是**页面对象，但它**拥有**多个页面对象

---

## 第四章：函数进阶 — 装饰器、生成器与上下文管理器

### 4.1 装饰器：在不改代码的情况下增强功能

项目中最重要的装饰器是 pytest 的标记装饰器：

```python
@pytest.mark.e2e          # 标记为端到端测试
@pytest.mark.wms          # 标记为 WMS 系统测试
def test_wms_login_success(require_live_ui, wms_flow, app_config, live_page):
    ...
```

🔑 **知识点：装饰器本质**
- `@decorator` 是语法糖，等价于 `func = decorator(func)`
- 装饰器是一个"函数的函数"——接收一个函数，返回一个增强版的函数
- pytest 用装饰器给测试函数打标签，运行时根据标签筛选

项目中更复杂的装饰器——tenacity 自动重试：

```python
# ai/provider.py
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

def __init__(self, settings: AISettings) -> None:
    self.session = requests.Session()
    self._do_request = retry(
        stop=stop_after_attempt(settings.max_retries),    # 最多重试 N 次
        wait=wait_exponential(multiplier=2, min=2, max=30),  # 指数退避等待
        reraise=True,                                     # 重试耗尽后重新抛出异常
    )(self._do_request)   # 把重试装饰器动态应用到 _do_request 方法上
```

🔑 **知识点：动态装饰器应用**
- `retry(...)(self._do_request)` — 先调用 `retry()` 得到装饰器，再把它应用到方法上
- 这跟 `@retry(...)` 效果一样，但可以在 `__init__` 中根据配置动态决定参数
- 指数退避：2s → 4s → 8s → 16s → 30s，越来越慢地重试

### 4.2 上下文管理器：自动清理资源

```python
# core/browser.py
from contextlib import contextmanager

class BrowserSessionManager:

    @contextmanager
    def page_session(self) -> Iterator[Page]:
        """创建并管理一个独立的浏览器页面会话。"""
        # ---- 进入 with 块之前执行 ----
        self.artifact_manager.ensure_directories()
        with sync_playwright() as playwright:
            browser = browser_type.launch(**launch_kwargs)
            context = browser.new_context(record_video_dir=str(...))
            page = context.new_page()
            try:
                yield page        # ← 暂停，把 page 交给 with 块使用
            finally:
                # ---- 退出 with 块之后执行 ----
                context.close()
                browser.close()
```

🔑 **知识点：上下文管理器与 yield**
- `@contextmanager` 装饰器把生成器函数变成上下文管理器
- `yield` 之前的代码 = `__enter__`（进入 with 块时执行）
- `yield` 之后的代码 = `__exit__`（退出 with 块时执行，包括异常情况）
- `finally` 确保无论是否出错都会关闭浏览器

使用方式（conftest.py）：
```python
@pytest.fixture()
def live_page(browser_manager, require_live_ui):
    with browser_manager.page_session() as page:
        yield page    # pytest 拿到 page，注入给测试用例
```

🔑 **知识点：with 语句**
- `with X as Y:` — 自动管理资源的获取和释放
- 即使 with 块中出了异常，也会确保清理代码执行
- 常见场景：文件操作、数据库连接、浏览器会话

### 4.3 生成器：yield 的另一面

```python
# conftest.py 中的 fixture
@pytest.fixture()
def live_page(browser_manager, require_live_ui):
    with browser_manager.page_session() as page:
        yield page    # ← 这是一个生成器 fixture
```

🔑 **知识点：pytest 的生成器 fixture**
- 用 `yield` 而非 `return` 的 fixture 会在测试后执行清理
- `yield` 之前 = setup（准备），`yield` 之后 = teardown（清理）
- 这是 pytest 推荐的资源管理模式

---

## 第五章：类型系统与数据模型

### 5.1 类型注解：给代码加注释

项目中的类型注解随处可见：

```python
def fill(self, name: str, value: str, candidates: list[LocatorCandidate], context: str) -> None:
```

🔑 **知识点：类型注解语法**
- 参数注解：`name: str` — 告诉读者 name 应该是字符串
- 返回值注解：`-> None` — 这个函数不返回任何值
- 复杂类型：`list[LocatorCandidate]` — 元素为 LocatorCandidate 的列表
- 可选类型：`AISettings | None` — 可以为 AISettings 或 None（Python 3.10+）
- 字典类型：`dict[str, Any]` — 键为 str、值为任意类型的字典

### 5.2 dataclass：轻量数据容器

```python
from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass(slots=True)
class AIResponse:
    """模型调用的统一响应体。"""
    success: bool
    content: dict[str, Any]
    raw_text: str = ""           # 有默认值的字段放在后面
    error: str = ""

@dataclass(slots=True)
class LocatorCandidate:
    """定位候选项。"""
    name: str
    selector: str
    kind: str = "locator"        # 默认值

@dataclass(slots=True)
class DecisionTrace:
    """AI 决策轨迹记录。"""
    action: str
    mode: str
    success: bool
    context_summary: str
    result_summary: str
    fallback_action: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)  # 可变默认值用 field

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)       # 自动转成字典
```

🔑 **知识点：dataclass 详解**
- `@dataclass` 自动生成 `__init__`、`__repr__`、`__eq__` 等方法
- `slots=True`：使用 `__slots__` 代替 `__dict__`，更省内存、更快
- 有默认值的字段必须放在没有默认值的字段后面
- `field(default_factory=dict)`：可变默认值必须用工厂函数（避免所有实例共享同一个字典）
- `asdict(obj)`：将 dataclass 实例转为字典

### 5.3 Pydantic：带校验的数据模型

```python
from pydantic import BaseModel, Field

class ExecutionSettings(BaseModel):
    browser: str = "chromium"
    headless: bool = False
    slow_mo: int = 0
    default_timeout_ms: int = 10_000

class AppConfig(BaseModel):
    environment: str                    # 必填字段
    systems: Dict[str, SystemEndpoint]  # 嵌套模型
    execution: ExecutionSettings        # 嵌套模型
    reporting: ReportingSettings
    ai: AISettings
    api: ApiSettings
    credentials: CredentialSettings
```

🔑 **知识点：Pydantic vs dataclass**
- **dataclass**：纯数据容器，不做校验，轻量快速
- **Pydantic BaseModel**：数据容器 + 类型校验 + 序列化/反序列化
- `AppConfig.model_validate(raw)` — 自动校验 YAML 数据是否符合模型定义
- 不符合时会抛出 `ValidationError`，告诉你哪个字段、什么问题

项目中的分工：
- `ai/models.py` 的数据结构用 **dataclass**（纯内存传递，不需要校验外部输入）
- `core/config/models.py` 的配置模型用 **Pydantic**（需要校验 YAML 文件中的外部输入）

---

## 第六章：异常处理与容错机制

### 6.1 try-except-else-finally 完整结构

```python
# main.py cmd_check 中的典型用法
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        for browser in browsers:
            try:
                getattr(p, browser).launch()
                print(f"[OK] Playwright {browser} 浏览器可用")
            except Exception:
                print(f"[WARN] Playwright {browser} 未安装")
except Exception as exc:
    print(f"[ERROR] Playwright 检查失败: {exc}")
```

🔑 **知识点：异常处理层级**
- 可以嵌套 try-except
- `except Exception as exc`：捕获异常对象，可以读取错误信息
- 项目中"外层兜底，内层细分"的模式很常见

### 6.2 项目中的容错策略

```python
# ai/locator.py — 三阶段容错
def resolve(self, page, candidates, context):
    # 阶段1：规则定位（快速、免费）
    for candidate in candidates:
        if self._matches(page, candidate.selector):
            return LocatorResolution(candidate.selector, "rule", True, trace)

    # 阶段2：AI 自愈（慢速、付费、但智能）
    if self.ai_settings.mode == "disabled" or not self.provider:
        return LocatorResolution("", "none", False, trace)  # 优雅降级

    response = self.provider.complete_json("heal_locator", payload)
    selector = response.content.get("selector", "")
    success = bool(selector and self._matches(page, selector))

    # 阶段3：AI 结果仍需在真实页面上二次校验
    return LocatorResolution(selector, "ai", success, trace)
```

🔑 **知识点：容错设计模式**
- **快速失败**：规则定位先试，成功即返回
- **优雅降级**：AI 不可用时不崩溃，返回失败结果
- **二次校验**：AI 的结果不盲信，回到真实环境验证
- **审计追踪**：每次决策都记录 DecisionTrace，方便事后排查

---

## 第七章：pytest 测试框架深度解析

### 7.1 测试用例极简的秘密：fixture 依赖注入

看一个测试用例有多简洁：

```python
@pytest.mark.e2e
@pytest.mark.wms
def test_wms_login_success(require_live_ui, wms_flow, app_config, live_page):
    """验证 WMS 登录后成功跳转到首页并显示'首页'文本。"""
    wms = app_config.systems["wms"]
    wms_flow.login(wms.base_url, wms.login_path,
                   app_config.credentials.wms_username,
                   app_config.credentials.wms_password)
    live_page.wait_for_url("**/dropshipping/home", timeout=30000)
    assert "/dropshipping/home" in live_page.url
    assert "首页" in live_page.locator("body").inner_text()
```

测试函数的4个参数都不是自己创建的，全部由 conftest.py 的 fixture 自动注入：

| 参数 | fixture 作用 | scope |
|------|-------------|-------|
| `require_live_ui` | 检查 UI 测试是否启用，未启用则跳过 | function |
| `wms_flow` | 组装完整的 WMS 业务流对象 | function |
| `app_config` | 加载全局配置 | session |
| `live_page` | 提供独立的浏览器页面 | function |

### 7.2 fixture 的 scope 生命周期

```python
@pytest.fixture(scope="session")      # 整个测试会话只创建一次
def app_config(project_root):
    return ConfigLoader(project_root).load(...)

@pytest.fixture(scope="session")      # 整个测试会话只创建一次
def ai_provider(app_config):
    return OpenAICompatibleProvider(app_config.ai)

@pytest.fixture()                      # 每个测试函数创建一次（默认 scope="function"）
def live_page(browser_manager, require_live_ui):
    with browser_manager.page_session() as page:
        yield page

@pytest.fixture()                      # 每个测试函数创建一次
def wms_flow(live_page, locator_strategy, ...):
    return WMSWarehouseFlow(...)
```

🔑 **知识点：fixture scope**
- `session`：整个 pytest 运行期间只创建一次，所有测试共享（如配置、AI provider）
- `function`：每个测试函数创建一次，测试间互不干扰（如浏览器页面）
- fixture 可以依赖其他 fixture，pytest 自动按依赖关系排序

### 7.3 conftest.py 的魔法

```
tests/
├── conftest.py          ← 全局 fixture 定义在这里
├── wms/
│   └── test_login.py    ← 可以直接使用 conftest.py 中的 fixture
├── oms/
│   └── test_login.py    ← 同样可以使用
└── cross_system/
    └── test_fulfillment.py  ← 同样可以使用
```

🔑 **知识点：conftest.py 规则**
- pytest 自动发现 `conftest.py`，不需要 import
- `conftest.py` 中的 fixture 对同目录及子目录的所有测试可见
- 可以有多层 conftest.py，子目录的可以覆盖父目录的

### 7.4 pytest 标记系统

```python
# pyproject.toml 中定义标记
[tool.pytest.ini_options]
markers = [
  "e2e: end-to-end UI automation cases",
  "oms: OMS domain test cases",
  "wms: WMS domain test cases",
  "cross_system: Cross-system flow cases",
  "smoke: minimal contract validation cases",
]

# 使用标记
@pytest.mark.e2e
@pytest.mark.wms
def test_wms_login_success(...):
    ...

# 运行时筛选
# pytest -m e2e          只运行标记为 e2e 的测试
# pytest -m wms          只运行标记为 wms 的测试
# pytest -m "e2e and wms" 运行同时标记为 e2e 和 wms 的测试
```

---

## 第八章：AI 模块 — 把所有知识串起来

### 8.1 AI 模块架构全景

```
ai/
├── models.py           ← 数据结构（dataclass）
├── provider.py         ← AI 调用（ABC + 继承 + 装饰器 + 异常处理）
├── locator.py          ← 自愈定位（策略模式 + 容错 + 审计）
├── assertion.py        ← 智能断言
├── failure_analysis.py ← 失败分析
└── report_enricher.py  ← 报告增强
```

### 8.2 provider.py — 一个文件浓缩所有知识点

让我们用学到的知识重新审视这个文件：

```python
from abc import ABC, abstractmethod          # ← 抽象基类（第三章）
from dataclasses import asdict               # ← dataclass（第五章）
import json, re                              # ← 标准库（第二章）
from typing import Any                       # ← 类型注解（第五章）
import requests                              # ← 第三方库
from tenacity import retry, ...              # ← 装饰器（第四章）

class AIProvider(ABC):                       # ← 抽象基类（第三章）
    @abstractmethod                          # ← 抽象方法（第三章）
    def complete_json(self, task, payload) -> AIResponse:  # ← 类型注解（第五章）
        raise NotImplementedError

class OpenAICompatibleProvider(AIProvider):  # ← 继承（第三章）
    TASK_PROMPTS: dict[str, str] = { ... }   # ← 类变量（第三章）

    def __init__(self, settings: AISettings): # ← 构造函数（第三章）
        self._do_request = retry(            # ← 装饰器动态应用（第四章）
            stop=stop_after_attempt(settings.max_retries),
            wait=wait_exponential(multiplier=2, min=2, max=30),
            reraise=True,
        )(self._do_request)

    def complete_json(self, task, payload) -> AIResponse:  # ← 实现抽象方法
        try:                                 # ← 异常处理（第六章）
            response = self._do_request(body)
            raw = response.json()
            message = raw["choices"][0]["message"]["content"]  # ← 字典操作（第二章）
            message = self._extract_json_text(message)         # ← 调用静态方法
            content = json.loads(message)
            return AIResponse(success=True, content=content, raw_text=message)  # ← dataclass
        except Exception as exc:             # ← 异常处理（第六章）
            return AIResponse(success=False, content={}, error=str(exc))

    @staticmethod                            # ← 静态方法（第三章）
    def _extract_json_text(text: str) -> str:
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip()    # ← 正则表达式
        return text
```

### 8.3 自愈定位器 — 项目最精彩的设计

```
用户调用 self.fill("用户名", "admin", candidates, "WMS登录用户名")
        ↓
BasePage.fill() → BasePage.smart_locator()
        ↓
SelfHealingLocator.resolve()
        ↓
  ┌─────────────────────────────────────┐
  │ 阶段1：规则定位（遍历 candidates）   │
  │   #username 命中？→ 返回             │
  │   input[name='username'] 命中？→ 返回 │
  │   ...全部未命中 ↓                    │
  │                                     │
  │ 阶段2：AI 自愈                      │
  │   AI 模式=disabled？→ 返回失败       │
  │   提取 DOM → 调用大模型 → 获得选择器  │
  │                                     │
  │ 阶段3：二次校验                      │
  │   在真实页面上验证 AI 返回的选择器     │
  │   验证通过？→ 返回成功               │
  │   验证失败？→ 返回失败               │
  │                                     │
  │ 全程：记录 DecisionTrace 审计日志     │
  └─────────────────────────────────────┘
```

这个设计用到了我们学过的几乎所有知识：
- **继承**：SelfHealingLocator 继承 LocatorStrategy
- **抽象基类**：LocatorStrategy 定义了 resolve 接口
- **dataclass**：LocatorCandidate、LocatorResolution、DecisionTrace
- **异常处理**：`_matches` 中的 try-except
- **装饰器**：tenacity 自动重试
- **字典操作**：provider 与 AI API 交互
- **上下文管理器**：浏览器页面的自动清理
- **类型注解**：贯穿所有函数签名

---

## 🎯 学习路线建议

### 第一周：读懂项目流程
1. 从 `main.py` → `run_all_scenarios.py` → `conftest.py` → `test_login.py` 追踪一遍
2. 理解"命令行 → pytest → fixture → 测试函数"的完整调用链

### 第二周：掌握基础语法
1. 对照第二章，在项目中找到每种语法的实际使用
2. 尝试修改一个测试用例，观察运行结果

### 第三周：理解面向对象
1. 画出 BasePage → WMSLoginPage 的继承关系
2. 理解"组合"模式在 Flow 层的应用
3. 尝试新建一个页面对象（比如 WMSHomePage）

### 第四周：深入进阶特性
1. 理解 fixture 的依赖注入机制
2. 理解上下文管理器如何管理浏览器生命周期
3. 理解装饰器（pytest.mark 和 tenacity）的工作原理

### 第五周+：AI 模块实战
1. 配置 AI_API_KEY，启用 AI 增强模式
2. 观察自愈定位器如何工作
3. 阅读审计日志，理解决策轨迹

---

## 📌 Python 速查表（按项目中的使用频率排序）

| 语法 | 项目示例 | 重要性 |
|------|---------|--------|
| `def` 函数定义 | `def login(self, username, password)` | ⭐⭐⭐⭐⭐ |
| `class` 类定义 | `class WMSLoginPage(BasePage)` | ⭐⭐⭐⭐⭐ |
| `import` 导入 | `from pathlib import Path` | ⭐⭐⭐⭐⭐ |
| `if/else` 条件 | `if not resolution.success:` | ⭐⭐⭐⭐⭐ |
| `for` 循环 | `for candidate in candidates:` | ⭐⭐⭐⭐⭐ |
| `try/except` | `except Exception as exc:` | ⭐⭐⭐⭐⭐ |
| f-string | `f"[OK] Playwright {browser} 可用"` | ⭐⭐⭐⭐⭐ |
| `dict` 字典 | `target_map = {"all": [], ...}` | ⭐⭐⭐⭐ |
| `list` 列表 | `command = [sys.executable, "-m", "pytest"]` | ⭐⭐⭐⭐ |
| `with` 上下文管理 | `with sync_playwright() as p:` | ⭐⭐⭐⭐ |
| `@decorator` 装饰器 | `@pytest.mark.wms` | ⭐⭐⭐⭐ |
| `yield` 生成器 | `yield page` | ⭐⭐⭐ |
| `@dataclass` | `@dataclass(slots=True) class AIResponse` | ⭐⭐⭐ |
| Pydantic `BaseModel` | `class AppConfig(BaseModel)` | ⭐⭐⭐ |
| ABC 抽象基类 | `class AIProvider(ABC)` | ⭐⭐⭐ |
| `super()` | `super().__init__(...)` | ⭐⭐⭐ |
| 类型注解 | `def fill(self, name: str) -> None:` | ⭐⭐⭐ |
| `**kwargs` 解包 | `browser_type.launch(**launch_kwargs)` | ⭐⭐ |
| `staticmethod` | `@staticmethod def _extract_json_text(...)` | ⭐⭐ |
| `__name__ == "__main__"` | 入口守卫 | ⭐⭐ |
