<!-- 中文说明：本文件提供项目的最快上手路径和常用命令。 -->
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

## 5. 一键执行所有场景

当项目后续接入更多页面和流程后，不需要按文件单独执行。统一使用下面的入口即可串行运行全部 `e2e` 场景：

```bash
python -m uv run run-all-scenarios
```

Windows 下也可以直接运行：

```bat
run_all.cmd
```

也支持指定运行范围：

```bat
run_all.cmd all
run_all.cmd wms
run_all.cmd oms
run_all.cmd cross_system
run_all.cmd smoke
run_all.cmd tests\wms\test_login.py
run_all.cmd wms -k login
```

说明：

- `run_all.cmd` 只是 Windows 启动壳
- `src/utils/run_all_scenarios.py` 才是统一运行入口
- 这样做是为了避免批处理文件在不同编码环境下因为中文注释而影响执行

## 6. 常用目录

- 日志：`artifacts/logs`
- 截图：`artifacts/screenshots`
- 视频：`artifacts/videos`
- HTML 报告：`artifacts/reports`
