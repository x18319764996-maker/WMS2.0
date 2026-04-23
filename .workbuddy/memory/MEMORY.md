# WMS2.0 项目记忆

## 项目概述
**项目名称**: WMS + OMS AI 增强型 UI 自动化框架  
**技术栈**: Python 3.11+ / Playwright / Pytest / AI增强  
**主要目标**: 企业级WMS(仓储管理系统)和OMS(订单管理系统)双系统UI自动化测试

## 核心架构特点

### 1. 五层分层架构
- **运行入口层**: run_all.cmd + run_all_scenarios.py
- **pytest装配层**: conftest.py 全局依赖注入
- **基础能力层**: core/browser、ai/provider、config/loader
- **页面与业务流层**: pages + flows + components
- **测试用例层**: tests/{oms,wms,cross_system,smoke}

### 2. AI增强能力
- **智能定位**: SelfHealingLocator 支持规则+AI双重定位
- **自愈机制**: 定位失败时自动调用AI识别元素
- **失败分析**: AI辅助分析测试失败原因
- **报告增强**: AI生成诊断信息补充报告
- **模式切换**: disabled/enhanced 两种运行模式

### 3. 技术亮点
- **依赖注入**: pytest fixture统一装配，测试用例极简
- **浏览器管理**: 上下文隔离、视频录制、超时控制
- **环境隔离**: YAML配置 + .env + 环境变量三层配置
- **UI/API一体化**: 同时支持UI和API校验
- **跨系统流程**: 支持OMS→WMS跨系统业务流测试

## 项目结构

```
WMS2.0/
├── config/           # 环境配置(test.yaml, prod.yaml)
├── docs/             # 中文文档
├── src/              # 核心代码(src layout)
│   ├── ai/           # AI能力(provider, locator, assertion, failure_analysis)
│   ├── api/          # API客户端(oms_client, wms_client)
│   ├── components/   # 可复用控件(table, dialog, date_picker等)
│   ├── core/         # 基础设施(browser, config, logging, artifacts)
│   ├── data/         # 测试数据加载
│   ├── domains/      # 业务域模型
│   ├── flows/        # 业务流层(oms, wms, cross_system)
│   ├── pages/        # 页面对象层(oms, wms)
│   ├── templates/    # 模板
│   └── utils/        # 工具函数
├── tests/            # 测试用例
│   ├── oms/          # OMS系统测试
│   ├── wms/          # WMS系统测试
│   ├── cross_system/ # 跨系统测试
│   └── smoke/        # 冒烟测试
└── artifacts/        # 测试产物(日志、截图、视频、报告)
```

## 运行方式

### 1. 统一入口
```bash
run_all.cmd all          # 全部场景
run_all.cmd wms          # WMS场景
run_all.cmd oms          # OMS场景
run_all.cmd cross_system # 跨系统场景
run_all.cmd smoke        # 冒烟测试
```

### 2. 直接pytest
```bash
set ENABLE_LIVE_UI=true
set TEST_ENV=test
uv run pytest tests/wms/test_login.py -q -s
```

### 3. 关键环境变量
- `ENABLE_LIVE_UI`: 是否启用真实UI测试
- `TEST_ENV`: 环境选择(test/prod)
- `AI_MODE`: AI模式(disabled/enhanced)
- `HEADLESS`: 无头模式(true/false)

## 关键依赖
- playwright>=1.52.0
- pytest>=8.3.5
- pydantic>=2.8.2
- allure-pytest>=2.13.5
- requests>=2.32.3
- tenacity>=9.0.0

## 开发规范
- 使用中文注释标记模块用途
- 采用src layout布局
- pytest marker标记用例类型(e2e, wms, oms, cross_system, smoke)
- BasePage和BaseFlow作为基类
- 通过fixture注入依赖，避免在测试用例中直接实例化

## 已实现功能
✅ 完整的五层架构  
✅ AI智能定位与自愈  
✅ 浏览器会话管理  
✅ 配置分层加载  
✅ 测试产物管理  
✅ OMS/WMS登录场景  
✅ 跨系统订单履约流程  
✅ 多种复杂组件封装(table/dialog/date_picker等)

## 待扩展方向
- 更多业务场景覆盖
- AI模型优化与成本控制
- 并行执行能力
- 测试数据工厂
- CI/CD深度集成
