<!-- 中文说明：本文件说明 Jenkins 场景下的运行步骤与归档方式。 -->
# Jenkins 集成说明

## 推荐执行步骤

```bash
uv sync
uv run playwright install --with-deps chromium
uv run pytest --collect-only
uv run pytest -m e2e --html=artifacts/reports/pytest-report.html --self-contained-html
```

## 推荐环境变量

- `TEST_ENV=test`
- `ENABLE_LIVE_UI=true`
- `AI_MODE=enhanced`
- `AI_BASE_URL`
- `AI_API_KEY`
- `AI_MODEL`
- `OMS_USERNAME`
- `OMS_PASSWORD`
- `WMS_USERNAME`
- `WMS_PASSWORD`

## 归档建议

归档以下目录：

- `artifacts/` — 包含日志、截图、视频和 HTML 报告
- `allure-results/` — Allure 报告数据（如启用）

### AI 审计日志归档

当 `AI_MODE=enhanced` 时，每次模型调用会追加到 `artifacts/logs/ai_audit.jsonl`。该文件为 JSONL 格式（每行一条 JSON），记录内容包括：

- `action` — 决策动作类型（如 `resolve_locator`、`failure_analysis`）
- `prompt` — 发送给模型的提示词摘要
- `response` — 模型返回的结构化结果
- `latency_ms` — 本次调用耗时
- `timestamp` — 调用时间戳

建议在 Jenkins Pipeline 中将此文件与 `artifacts/` 一起归档，便于：

- 回溯 AI 决策路径
- 分析模型调用成功率和延迟
- 排查 AI 推断不准确的定位问题

## 注意事项

- Jenkins Linux 执行默认使用无头模式
- 路径处理必须走 `pathlib`
- 如运行环境缺依赖，优先使用 `playwright install --with-deps`
- AI 相关环境变量（`AI_BASE_URL`、`AI_API_KEY`、`AI_MODEL`）建议通过 Jenkins Credentials 注入，避免明文写入 Jenkinsfile