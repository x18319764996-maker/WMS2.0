<!-- 中文说明：本文件是项目总览文档，介绍框架目标、结构和基础运行方法。 -->
# WMS + OMS AI 增强型 UI 自动化框架

这是一个基于 `Python + Playwright + Pytest` 的企业级 UI 自动化框架骨架，面向 `WMS` 和 `OMS` 双系统场景，强调以下能力：

- 业务域组织 + Page Object + Flow 分层
- UI + API 一体化校验
- AI 增强定位、自愈、失败分析与报告增强
- 本地 Windows 调试与 Jenkins Linux 落地
- 适合测试团队多人协作和长期维护

## 目录说明

- `config/`：环境、日志和运行配置
- `docs/`：中文使用文档、扩展指南和 Jenkins 说明
- `src/`：核心框架代码
- `tests/`：示例用例与 smoke 校验
- `artifacts/`：日志、截图、视频和报告归档目录

## 快速开始

1. 安装 Python 3.11+。
2. 安装 `uv`。
3. 复制 `.env.example` 为 `.env` 并填写真实账号和 AI 参数。
4. 执行：

```bash
uv sync
uv run playwright install chromium
uv run pytest --collect-only
```

如需真实执行 UI 用例，请显式开启：

```bash
set ENABLE_LIVE_UI=true
uv run pytest -m e2e
```

如果希望以后统一执行所有已接入的场景，直接使用项目总入口：

```bash
python -m uv run run-all-scenarios
```

Windows 下也可以直接执行：

```bat
run_all.cmd
```

如果你想指定运行范围，也可以在后面追加目标参数：

```bat
run_all.cmd all
run_all.cmd wms
run_all.cmd oms
run_all.cmd cross_system
run_all.cmd smoke
run_all.cmd tests\wms\test_login.py
run_all.cmd wms -k login
```

补充说明：

- `run_all.cmd` 是 Windows 下的轻量启动脚本，本身只负责透传参数
- 真正的统一运行逻辑在 [run_all_scenarios.py](src/utils/run_all_scenarios.py)
- 为了避免 `cmd` 编码差异影响执行，批处理脚本保持极简，中文说明集中放在 Python 入口和文档中
- 详细脚本说明见 [run_all.cmd.md](run_all.cmd.md)

Linux/Jenkins 可参考 [docs/jenkins.md](docs/jenkins.md)。

## 默认运行约定

- 本地默认：有头运行，便于调试
- Jenkins 默认：无头运行，便于持续集成
- AI 默认：`enhanced`
- 配置模式：`.env + YAML`

## 文档入口

- [快速开始](docs/quick_start.md)
- [项目运行逻辑说明](docs/project_runtime_logic.md)
- [环境接入说明](docs/integration.md)
- [二次开发指南](docs/secondary_dev.md)
- [新增用例模板](docs/case_template.md)
- [业务域扩展规范](docs/domain_extension.md)
- [Jenkins 集成说明](docs/jenkins.md)
