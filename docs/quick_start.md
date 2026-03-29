# 快速开始

## 1. 环境准备

- Python 3.11+
- Windows 本地调试环境或 Linux Jenkins 执行环境
- 可访问目标系统的网络
- 可用的 OMS/WMS 账号
- 可选的 OpenAI 兼容模型服务

## 2. 初始化

1. 复制 `.env.example` 为 `.env`
2. 根据实际环境调整 `config/test.yaml` 或 `config/prod.yaml`
3. 执行：

```bash
uv sync
uv run playwright install chromium
```

## 3. 最小验证

```bash
uv run pytest --collect-only
uv run python -m compileall src tests
```

## 4. 启动真实 UI 用例

```bash
set ENABLE_LIVE_UI=true
set TEST_ENV=test
uv run pytest -m e2e
```

## 5. 常用目录

- 日志：`artifacts/logs`
- 截图：`artifacts/screenshots`
- 视频：`artifacts/videos`
- HTML 报告：`artifacts/reports`