<!-- 中文说明：本文档用于系统说明项目的整体运行逻辑、分层职责和常见执行路径。 -->
# 项目运行逻辑说明

## 1. 文档目的

本文档用于帮助项目成员快速理解当前 `WMS + OMS AI 增强型 UI 自动化框架` 的运行方式，重点说明以下内容：

- 项目从命令启动到测试执行完成的完整链路
- 各层模块分别负责什么
- 配置、浏览器、AI、业务流、测试用例之间如何协作
- 常用运行命令分别会触发哪些内部步骤
- 排查问题时应该优先看哪些文件

本文档更偏“运行机制说明”，不是接口字典，也不是业务需求文档。

## 2. 整体架构总览

当前项目可以拆成 5 层：

1. 运行入口层
2. `pytest` 装配层
3. 基础能力层
4. 页面与业务流层
5. 测试用例层

它们的调用关系如下：

```text
run_all.cmd / pytest 命令
        |
        v
run_all_scenarios.py
        |
        v
pytest 启动
        |
        v
tests/conftest.py
  - 加载配置
  - 初始化日志
  - 初始化 AI Provider
  - 初始化定位策略
  - 初始化 API Client
  - 初始化 BrowserSessionManager
  - 组装 OMS / WMS / CrossSystem Flow
        |
        v
tests/*.py 测试用例
        |
        v
flows/*.py 业务流
        |
        v
pages/*.py 页面对象 + api/*.py 接口客户端
        |
        v
core/*.py / ai/*.py / components/*.py
        |
        v
artifacts/ 产物输出（日志、截图、视频、报告）
```

一句话理解就是：

- 入口层决定“跑什么”
- `pytest` 装配层决定“怎么把对象都准备好”
- 业务流决定“业务步骤怎么串”
- 页面层决定“具体怎么点页面”
- 基础能力层决定“浏览器、配置、AI、报告怎么支撑”

## 3. 目录与模块职责

### 3.1 根目录

- [pyproject.toml](C:\Users\26582\Desktop\WMS2.0\pyproject.toml)
  - 定义依赖、打包方式、`pytest` 配置和统一命令入口
- [run_all.cmd](C:\Users\26582\Desktop\WMS2.0\run_all.cmd)
  - Windows 下的统一启动脚本
- [run_all.cmd.md](C:\Users\26582\Desktop\WMS2.0\run_all.cmd.md)
  - `run_all.cmd` 的中文说明文档
- [README.md](C:\Users\26582\Desktop\WMS2.0\README.md)
  - 项目总览说明

### 3.2 `config/`

- [test.yaml](C:\Users\26582\Desktop\WMS2.0\config\test.yaml)
  - 测试环境配置
- [prod.yaml](C:\Users\26582\Desktop\WMS2.0\config\prod.yaml)
  - 生产环境配置

主要承载：

- 系统地址
- 登录路径
- 浏览器执行参数
- AI 默认模式
- 报告、超时等运行参数

### 3.3 `src/`

`src/` 是核心代码目录，当前使用 `src layout` 结构。

重点子目录如下：

- `src/core/`
  - 基础设施，例如配置加载、浏览器管理、日志、产物管理
- `src/ai/`
  - AI Provider、智能定位、自愈、失败分析、报告增强
- `src/api/`
  - OMS/WMS 接口客户端
- `src/components/`
  - 可复用复杂控件封装，例如弹窗、表格、日期控件、树等
- `src/pages/`
  - 页面对象层，按 `oms`、`wms` 分开
- `src/flows/`
  - 业务流层，负责串业务步骤
- `src/utils/`
  - 通用工具与统一运行入口
- `src/data/`
  - 测试数据和共享数据能力

### 3.4 `tests/`

测试目录按业务域划分：

- `tests/oms/`
- `tests/wms/`
- `tests/cross_system/`
- `tests/smoke/`

这种组织方式的好处是：

- 符合业务域认知
- 便于统一入口按域运行
- 便于 Jenkins 分组和后续回归策略扩展

### 3.5 `artifacts/`

这个目录用于产出运行结果，包括：

- 日志
- 截图
- 视频
- HTML 报告

## 4. 运行入口层

运行入口主要有两种：

1. 直接执行 `pytest`
2. 通过统一入口执行

### 4.1 直接执行 `pytest`

适合：

- 单独调试某个测试文件
- 调试某条具体场景

例如：

```cmd
python -m uv run pytest tests\wms\test_login.py -q -s
```

### 4.2 统一入口

统一入口在这里：

- [run_all.cmd](C:\Users\26582\Desktop\WMS2.0\run_all.cmd)
- [run_all_scenarios.py](C:\Users\26582\Desktop\WMS2.0\src\utils\run_all_scenarios.py)

作用是：

- 统一拼装 `pytest` 命令
- 统一处理默认环境变量
- 按目标域运行测试
- 支持 `all / oms / wms / cross_system / smoke`
- 支持 `-k` 关键字过滤

例如：

```cmd
run_all.cmd
run_all.cmd wms
run_all.cmd wms -k login
run_all.cmd smoke
```

### 4.3 统一入口内部逻辑

[run_all_scenarios.py](C:\Users\26582\Desktop\WMS2.0\src\utils\run_all_scenarios.py) 主要做三件事：

1. 解析命令行参数
2. 把目标名称映射成测试路径
3. 组装并执行最终的 `pytest` 命令

核心函数：

- `build_parser`
- `resolve_target`
- `main`

## 5. pytest 装配层

`pytest` 启动后，核心装配逻辑在：

- [conftest.py](C:\Users\26582\Desktop\WMS2.0\tests\conftest.py)

这个文件的职责可以理解为“全局依赖装配中心”。

它负责初始化：

- 项目根目录
- 日志系统
- 全局配置
- 产物目录管理
- AI Provider
- 智能定位策略
- 断言助手
- 失败分析代理
- OMS/WMS API Client
- 浏览器管理器
- 业务流对象

所以测试文件本身可以尽量轻，只专注表达业务场景。

### 5.1 关键夹具

重点关注这些夹具：

- `project_root`
- `setup_logging`
- `app_config`
- `artifact_manager`
- `ai_provider`
- `locator_strategy`
- `assertion_assistant`
- `failure_analysis_agent`
- `browser_manager`
- `live_page`
- `oms_flow`
- `wms_flow`
- `cross_system_flow`

### 5.2 为什么真实 UI 用例有时会被跳过

项目默认不会直接跑真实页面。

只有当环境变量显式开启：

```cmd
set ENABLE_LIVE_UI=true
```

依赖真实页面的用例才会执行。

否则，`conftest.py` 中的 `require_live_ui` 夹具会统一跳过这些用例。

这样做的目的是：

- 避免没有账号时误跑
- 避免 Jenkins 或本地环境没准备好就访问真实系统
- 避免日常代码检查时误触发真实 UI 自动化

## 6. 配置加载逻辑

配置加载入口在：

- [loader.py](C:\Users\26582\Desktop\WMS2.0\src\core\config\loader.py)

### 6.1 配置来源

项目当前采用分层配置：

1. YAML 环境配置
2. `.env`
3. 运行时环境变量覆盖

对应来源包括：

- [test.yaml](C:\Users\26582\Desktop\WMS2.0\config\test.yaml)
- [prod.yaml](C:\Users\26582\Desktop\WMS2.0\config\prod.yaml)
- [.env.example](C:\Users\26582\Desktop\WMS2.0\.env.example)
- 运行命令里的 `set TEST_ENV=...`、`set HEADLESS=...` 等

### 6.2 加载顺序

实际逻辑大致是：

1. 读取 `.env`
2. 根据 `TEST_ENV` 选择环境 YAML
3. 从环境变量覆盖账号密码
4. 从环境变量覆盖 AI 模式和模型参数
5. 从环境变量覆盖浏览器执行参数

### 6.3 关键方法

[loader.py](C:\Users\26582\Desktop\WMS2.0\src\core\config\loader.py) 中建议重点看：

- `load`
- `_read_yaml`
- `_build_credentials`
- `_build_ai_settings`
- `_apply_execution_overrides`

## 7. 浏览器管理逻辑

浏览器会话管理在：

- [browser.py](C:\Users\26582\Desktop\WMS2.0\src\core\browser.py)

核心类：

- `BrowserSessionManager`

核心方法：

- `page_session`

### 7.1 单次页面会话流程

执行真实 UI 用例时，大致流程如下：

1. 启动浏览器
2. 创建浏览器上下文 `context`
3. 创建单独页面 `page`
4. 把这个页面交给页面对象和业务流使用
5. 用例结束后关闭 `context` 和浏览器

### 7.2 为什么这样设计

这样做的好处是：

- 每条真实用例更独立
- 浏览器状态隔离更清晰
- 便于录制视频和保存截图
- 便于控制超时和上下文级参数

### 7.3 当前浏览器策略

项目当前支持：

- 使用 Playwright 管理浏览器
- 优先复用本机已安装的浏览器，例如 Edge

这样做的目的，是在浏览器二进制下载较慢时，仍然能先跑通真实场景。

## 8. AI 增强层逻辑

AI 模块主要在这里：

- [provider.py](C:\Users\26582\Desktop\WMS2.0\src\ai\provider.py)
- [locator.py](C:\Users\26582\Desktop\WMS2.0\src\ai\locator.py)
- [assertion.py](C:\Users\26582\Desktop\WMS2.0\src\ai\assertion.py)
- [failure_analysis.py](C:\Users\26582\Desktop\WMS2.0\src\ai\failure_analysis.py)
- [report_enricher.py](C:\Users\26582\Desktop\WMS2.0\src\ai\report_enricher.py)

### 8.1 各模块职责

- `provider.py`
  - 接外部大模型接口
- `locator.py`
  - 负责智能定位和定位自愈
- `assertion.py`
  - 负责 AI 辅助断言
- `failure_analysis.py`
  - 负责失败原因分析
- `report_enricher.py`
  - 负责把 AI 分析结果补充到报告中

### 8.2 AI 数据模型（`src/ai/models.py`）

AI 模块的数据流通过以下 5 个 dataclass 串联：

```text
AIResponse          模型调用的统一响应体（success / content / raw_text / latency_ms）
  ↓
DecisionTrace       AI 决策轨迹记录（action / input_summary / output_summary / duration_ms）
  ↓                 → 序列化后追加到 JSONL 审计日志
LocatorCandidate    定位候选项（selector / strategy / score）
  ↓
LocatorResult       定位最终结果（found / selector / method / confidence / ai_used）
  ↓
FailureAnalysis     失败分析结果（category / root_cause / suggestion / ai_used）
```

这些 dataclass 全部使用 `@dataclass(slots=True)` 优化内存，并通过 `asdict()` 序列化为字典供 JSON 输出。

### 8.3 审计日志格式

当 AI 处于 `enhanced` 模式时，`OpenAICompatibleProvider` 在每次模型调用后将 `DecisionTrace` 追加到 `artifacts/logs/ai_audit.jsonl`。

每行一条 JSON，结构示例：

```json
{
  "action": "resolve_locator",
  "input_summary": "DOM fragment: <div class='login-form'>...",
  "output_summary": "selector=#username, confidence=0.92",
  "duration_ms": 1230,
  "timestamp": "2025-01-15T10:30:45.123Z"
}
```

审计日志用途：

- 回溯每次 AI 决策的输入输出
- 分析模型推断准确率和平均延迟
- 排查定位自愈失败的具体原因

### 8.4 AI 在运行中的位置

AI 不是单独跑一层流程，而是嵌入在关键节点：

- 定位失败时辅助识别控件（`SelfHealingLocator` 三阶段：规则候选 → AI 推断 → 真实页面验证）
- 断言时辅助理解页面语义（`AssertionAssistant` 提交页面摘要给模型）
- 出错时辅助分析原因（`FailureAnalysisAgent` 调用模型或本地兜底）
- 报告生成时补充诊断信息（`ReportEnricher` 输出 AI 决策摘要）

### 8.5 运行模式

通过环境变量可以控制 AI 模式：

```cmd
set AI_MODE=disabled
set AI_MODE=enhanced
```

| 模式 | 行为 |
|------|------|
| `disabled` | 只走基础规则逻辑，完全不调用模型接口，不产生审计日志 |
| `enhanced` | 规则失败后调用大模型推断；断言和失败分析均请求模型；全程写审计日志 |

## 9. 页面对象与复杂控件层

### 9.1 页面对象层

页面对象在：

- [pages/oms](C:\Users\26582\Desktop\WMS2.0\src\pages\oms)
- [pages/wms](C:\Users\26582\Desktop\WMS2.0\src\pages\wms)

页面对象的职责是：

- 表达页面级操作
- 对页面元素定位进行封装
- 向业务流暴露更稳定的方法

例如：

- 登录页负责输入用户名、密码、点击登录
- 订单页负责创建订单、查询订单、读取状态

### 9.2 复杂控件层

复杂控件封装在：

- [components](C:\Users\26582\Desktop\WMS2.0\src\components)

例如：

- [dialog.py](C:\Users\26582\Desktop\WMS2.0\src\components\dialog.py)
- [drawer.py](C:\Users\26582\Desktop\WMS2.0\src\components\drawer.py)
- [table.py](C:\Users\26582\Desktop\WMS2.0\src\components\table.py)
- [date_picker.py](C:\Users\26582\Desktop\WMS2.0\src\components\date_picker.py)

这样做的目的是：

- 把复杂控件逻辑复用起来
- 降低页面对象的复杂度
- 增强定位和交互的一致性

## 10. 业务流层

业务流在：

- [flows/oms](C:\Users\26582\Desktop\WMS2.0\src\flows\oms)
- [flows/wms](C:\Users\26582\Desktop\WMS2.0\src\flows\wms)
- [flows/cross_system](C:\Users\26582\Desktop\WMS2.0\src\flows\cross_system)

业务流层的职责是：

- 把多个页面动作串起来
- 把 UI 操作和接口校验组合起来
- 表达完整业务步骤，而不是单个页面动作

例如跨系统流程：

- [order_fulfillment_flow.py](C:\Users\26582\Desktop\WMS2.0\src\flows\cross_system\order_fulfillment_flow.py)

这一层通常会串：

- OMS 登录
- OMS 创建订单
- WMS 接续处理
- 库存或出库校验

所以业务流是最贴近实际测试场景的一层。

## 11. 测试用例层

测试文件位于：

- [tests/oms](C:\Users\26582\Desktop\WMS2.0\tests\oms)
- [tests/wms](C:\Users\26582\Desktop\WMS2.0\tests\wms)
- [tests/cross_system](C:\Users\26582\Desktop\WMS2.0\tests\cross_system)
- [tests/smoke](C:\Users\26582\Desktop\WMS2.0\tests\smoke)

测试用例层通常只做三件事：

1. 调用业务流
2. 准备或读取测试数据
3. 验证关键结果

例如你已经实际跑通过的登录场景在：

- [test_login.py](C:\Users\26582\Desktop\WMS2.0\tests\wms\test_login.py)

这层应该尽量保持“场景表达清晰”，而不是塞太多底层细节。

## 12. 产物输出逻辑

产物管理在：

- [artifacts.py](C:\Users\26582\Desktop\WMS2.0\src\core\artifacts.py)

运行过程中，常见产物会输出到：

- `artifacts/logs`
- `artifacts/screenshots`
- `artifacts/videos`
- `artifacts/reports`

统一入口默认会生成：

- `artifacts/reports/pytest-report.html`

这些产物用于：

- 问题定位
- 失败复盘
- Jenkins 归档
- 团队共享执行结果

## 13. 常用命令与实际含义

### 13.1 只跑 WMS 登录

```cmd
cd /d C:\Users\26582\Desktop\WMS2.0
set ENABLE_LIVE_UI=true
set TEST_ENV=test
set AI_MODE=disabled
set HEADLESS=false
python -m uv run pytest tests\wms\test_login.py -q -s
```

实际含义：

- 开启真实 UI
- 使用测试环境
- 暂时关闭 AI 增强
- 使用有头模式
- 只执行 WMS 登录场景

### 13.2 跑全部场景

```cmd
cd /d C:\Users\26582\Desktop\WMS2.0
run_all.cmd
```

或：

```cmd
run_all.cmd all
```

实际含义：

- 调用统一入口
- 默认执行全部接入范围内的场景
- 默认除 `smoke` 外按 `e2e` 标记执行

### 13.3 统一入口按域执行

```cmd
run_all.cmd wms
run_all.cmd oms
run_all.cmd cross_system
run_all.cmd smoke
run_all.cmd wms -k login
```

实际含义：

- 只跑指定业务域
- 或进一步按关键字缩小范围

## 14. PyCharm 与命令行为什么有时不一致

命令行当前使用的是项目自己的虚拟环境解释器：

- [python.exe](C:\Users\26582\Desktop\WMS2.0\.venv\Scripts\python.exe)

如果 PyCharm 没有对齐这两个配置，就可能出现“命令行能跑、IDE 报红”的情况：

1. 解释器没选到项目 `.venv`
2. `src` 没有标记为 `Sources Root`

建议统一如下：

- 解释器使用：
  - [python.exe](C:\Users\26582\Desktop\WMS2.0\.venv\Scripts\python.exe)
- 把 [src](C:\Users\26582\Desktop\WMS2.0\src) 标记为 `Sources Root`

## 15. 阅读源码的建议顺序

如果要快速理解项目，建议按下面顺序阅读：

1. [run_all_scenarios.py](C:\Users\26582\Desktop\WMS2.0\src\utils\run_all_scenarios.py)
2. [conftest.py](C:\Users\26582\Desktop\WMS2.0\tests\conftest.py)
3. [loader.py](C:\Users\26582\Desktop\WMS2.0\src\core\config\loader.py)
4. [browser.py](C:\Users\26582\Desktop\WMS2.0\src\core\browser.py)
5. [locator.py](C:\Users\26582\Desktop\WMS2.0\src\ai\locator.py)
6. [test_login.py](C:\Users\26582\Desktop\WMS2.0\tests\wms\test_login.py)
7. 当前你最想打通的业务流文件

## 16. 总结

这个项目的运行逻辑可以概括为：

- 运行入口负责决定执行范围
- `pytest + conftest` 负责装配全局依赖
- `flow` 负责串联业务步骤
- `page / component` 负责具体页面交互
- `core / ai / api` 负责支撑能力
- `artifacts` 负责沉淀结果

从团队协作角度看，这种分层方式的价值在于：

- 便于多人并行维护
- 便于后续扩展更多页面和流程
- 便于把 UI、接口、AI 增强和报告能力整合到一个统一框架中

