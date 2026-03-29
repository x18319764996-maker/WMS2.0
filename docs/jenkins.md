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

- `artifacts/`
- `allure-results/`

## 注意事项

- Jenkins Linux 执行默认使用无头模式
- 路径处理必须走 `pathlib`
- 如运行环境缺依赖，优先使用 `playwright install --with-deps`