<!-- 中文说明：本文件说明如何接入真实环境、真实账号和 AI 服务。 -->
# 环境接入说明

## 配置分层

本项目采用 `.env + YAML` 分层：

- `.env`：账号、密码、AI Key、Base URL 等敏感信息
- `config/*.yaml`：环境 URL、超时、报告、接口模板等业务配置

## OMS / WMS 接入

需要至少补齐以下信息：

- OMS 登录地址
- WMS 登录地址
- OMS 关键接口模板
- WMS 关键接口模板
- 真实页面控件 locator 或稳定 test id

## AI 接入

默认 provider 为 OpenAI 兼容接口（支持 OpenAI、Azure、vLLM、GLM 等），需要在 `.env` 中提供：

- `AI_BASE_URL` — 模型服务端点，如 `https://api.meai.cloud/v1`
- `AI_API_KEY` — 身份凭证
- `AI_MODEL` — 模型名称，如 `glm-5`
- `AI_MAX_RETRIES` — 模型调用最大重试次数（可选，默认 3）

### AI 运行模式

通过环境变量 `AI_MODE` 控制 AI 参与程度：

| 模式 | 值 | 行为 |
|------|----|------|
| 关闭 | `disabled` | 完全不调用模型接口；定位仅走规则匹配，失败分析走本地分类（Timeout→timeout / 其他→ui_failure） |
| 增强 | `enhanced` | 规则候选失败后调用大模型推断 selector；断言场景提交页面摘要给模型；失败时请求模型分析根因 |

设置方式：

```bash
set AI_MODE=disabled    # 关闭 AI
set AI_MODE=enhanced    # 启用 AI 增强（默认）
```

### AI 功能在各模块的作用

- **定位自愈**（`src/ai/locator.py`）：三阶段流程——规则候选匹配 → AI 推断 → 真实页面二次校验
- **断言辅助**（`src/ai/assertion.py`）：将页面摘要与期望条件提交模型，获取可执行的断言建议
- **失败分析**（`src/ai/failure_analysis.py`）：模型分析异常根因和修复建议；AI 不可用时走本地兜底
- **报告增强**（`src/ai/report_enricher.py`）：将 AI 决策摘要写入独立 JSON 供后续分析
- **审计日志**（`src/ai/provider.py`）：每次模型调用以 JSONL 格式追加到 `artifacts/logs/ai_audit.jsonl`