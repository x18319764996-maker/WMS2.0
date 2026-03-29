<!-- 中文说明：本文件用于解释 run_all.cmd 的用途、参数、运行方式和后续扩展方法，不参与脚本执行。 -->
# run_all.cmd 使用说明

## 1. 文件作用

`run_all.cmd` 是 Windows 环境下的统一启动脚本，用来从项目根目录一键触发自动化测试运行入口。

它本身不负责复杂业务逻辑，只做三件事：

- 进入项目根目录
- 补齐基础环境变量默认值
- 把你传入的参数透传给 Python 统一运行入口

真正的执行逻辑在：

- [run_all_scenarios.py](C:\Users\26582\Desktop\WMS2.0\src\utils\run_all_scenarios.py)

## 2. 默认行为

当你直接执行：

```bat
run_all.cmd
```

脚本会自动补齐以下默认环境变量：

- `ENABLE_LIVE_UI=true`
- `TEST_ENV=test`
- `AI_MODE=disabled`
- `HEADLESS=false`

然后调用：

```bat
python -m uv run run-all-scenarios
```

这意味着默认行为是：

- 使用测试环境
- 运行真实 UI
- 关闭 AI 增强
- 使用有头模式

## 3. 支持的参数

### 3.1 不带参数

运行全部 `e2e` 场景：

```bat
run_all.cmd
```

### 3.2 内置目标参数

运行全部 E2E：

```bat
run_all.cmd all
```

只运行 OMS：

```bat
run_all.cmd oms
```

只运行 WMS：

```bat
run_all.cmd wms
```

只运行跨系统：

```bat
run_all.cmd cross_system
```

只运行 smoke：

```bat
run_all.cmd smoke
```

### 3.3 指定具体测试文件或目录

例如只运行一个测试文件：

```bat
run_all.cmd tests\wms\test_login.py
```

例如运行某个目录下的测试：

```bat
run_all.cmd tests\wms
```

### 3.4 按关键字过滤

例如只运行 WMS 里包含 `login` 关键字的测试：

```bat
run_all.cmd wms -k login
```

例如运行全部 E2E 中名称带 `inventory` 的测试：

```bat
run_all.cmd all -k inventory
```

## 4. 参数解析规则

`run_all.cmd` 自己不解析业务参数，它只是把参数原样传给 Python 入口：

```bat
python -m uv run run-all-scenarios %*
```

真正的参数解析逻辑由：

- [run_all_scenarios.py](C:\Users\26582\Desktop\WMS2.0\src\utils\run_all_scenarios.py)

负责。

当前规则如下：

- 第一个参数是 `target`
- `-k` 后面跟 pytest 关键字过滤条件

目前内置 `target` 映射关系如下：

- `all` -> 跑全部 E2E
- `oms` -> `tests/oms`
- `wms` -> `tests/wms`
- `cross_system` -> `tests/cross_system`
- `smoke` -> `tests/smoke`
- 其他值 -> 直接按 pytest 路径处理

## 5. 环境变量说明

### 5.1 脚本默认补齐的变量

如果你没有手动设置，脚本会自动补以下默认值：

- `ENABLE_LIVE_UI=true`
- `TEST_ENV=test`
- `AI_MODE=disabled`
- `HEADLESS=false`

### 5.2 你可以在运行前手工覆盖

例如：

```bat
set TEST_ENV=prod
set AI_MODE=enhanced
set HEADLESS=true
run_all.cmd wms
```

这样脚本不会覆盖你已经设置的值。

## 6. 推荐使用方式

### 6.1 本地开发调试

先跑稳定集：

```bat
run_all.cmd smoke
```

再跑某个业务域：

```bat
run_all.cmd wms
```

最后按关键字缩小范围：

```bat
run_all.cmd wms -k login
```

### 6.2 团队回归

统一执行：

```bat
run_all.cmd all
```

### 6.3 问题定位

当你只想复现某一个失败场景时：

```bat
run_all.cmd tests\wms\test_login.py
```

## 7. 扩展建议

如果将来你希望它更强，可以继续往下面这些方向扩展：

### 7.1 增加新的内置目标

例如：

- `regression`
- `sanity`
- `critical`

实现方式是在：

- [run_all_scenarios.py](C:\Users\26582\Desktop\WMS2.0\src\utils\run_all_scenarios.py)

里补充新的 `target_map` 映射。

### 7.2 支持更直观的关键字写法

例如你将来可能想支持：

```bat
run_all.cmd wms login
```

而不是：

```bat
run_all.cmd wms -k login
```

这可以在 Python 入口里继续增强参数解析逻辑。

### 7.3 支持不同运行模式

例如：

- 只跑稳定可过场景
- 只跑核心主链路
- 跑全量回归

这些都适合放到 Python 入口中实现，而不是放到 `.cmd` 里写复杂分支。

## 8. 为什么不直接在 run_all.cmd 里写大量中文注释

原因很实际：

- Windows `cmd` 对文件编码比较敏感
- 在当前环境里，批处理文件中的中文注释可能被误解析
- 这会导致脚本执行时冒出乱码报错

为了保证 `run_all.cmd` 零副作用、零功能影响，执行文件本体保持极简，中文说明集中放在这个文档里。

## 9. 相关文件

- 启动脚本：[run_all.cmd](C:\Users\26582\Desktop\WMS2.0\run_all.cmd)
- Python 统一入口：[run_all_scenarios.py](C:\Users\26582\Desktop\WMS2.0\src\utils\run_all_scenarios.py)
- 项目总说明：[README.md](C:\Users\26582\Desktop\WMS2.0\README.md)
- 快速开始：[quick_start.md](C:\Users\26582\Desktop\WMS2.0\docs\quick_start.md)
