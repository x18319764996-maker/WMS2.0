<!-- 中文说明：本文件说明如何按规范新增测试用例与模板文件。 -->
# 新增用例模板说明

新增 UI 自动化用例时，请遵循以下顺序：

1. 明确业务域：OMS / WMS / CrossSystem
2. 如果需要新页面，先补页面对象
3. 如果是复杂流程，先补 Flow
4. 准备测试数据文件
5. 编写测试用例，只表达业务意图和断言

## 推荐模板

- 页面对象模板：`src/templates/page_template.py`
- 流程模板：`src/templates/flow_template.py`
- 用例模板：`src/templates/test_template.py`

## 注解规范

新增文件必须遵循以下注解标准：

| 位置 | 要求 | 示例 |
|------|------|------|
| 模块顶部 | 中文 docstring，说明模块职责 | `"""WMS 登录页面对象，封装用户名/密码填写和登录提交操作。"""` |
| 类定义 | 中文 docstring，说明类职责和核心能力 | `"""WMS 登录页，包含打开登录页和提交登录凭据两个核心操作。"""` |
| 方法/函数 | 中文 docstring，一句话说明行为 | `"""填写用户名、密码并点击登录按钮。"""` |
| `__init__` | 说明注入了哪些依赖 | `"""注入 Playwright Page 和自愈定位策略。"""` |
| 行内注释 | `# 中文说明：` 前缀 | `# 中文说明：发送给模型的 DOM 片段最大字符数` |

## AI 定位候选声明

页面对象中定义 AI 候选 locator 时，建议使用以下格式：

```python
# 中文说明：候选 locator 按优先级排列，自愈定位器依次尝试
CANDIDATES_USERNAME = [
    "input[placeholder='用户名']",      # 中文说明：占位符定位
    "#username",                         # 中文说明：ID 定位
    "input[type='text']:first-child",   # 中文说明：类型 + 位置兜底
]
```

当所有候选均失败且 AI 处于 `enhanced` 模式时，`SelfHealingLocator` 会自动提取页面 DOM 片段调用大模型推断新 selector。