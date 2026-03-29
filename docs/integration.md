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

默认 provider 为 OpenAI 兼容接口，需要提供：

- `AI_BASE_URL`
- `AI_API_KEY`
- `AI_MODEL`

如果暂时不启用 AI，可设置：

```bash
set AI_MODE=disabled
```