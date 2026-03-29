<!-- 中文说明：本文件说明如何扩展新的业务域并保持目录与分层一致。 -->
# 业务域扩展规范

## 目录规则

每新增一个业务域，必须同时考虑以下层级：

- `src/domains/<domain>`：领域模型、上下文、业务约束
- `src/pages/<domain>`：页面对象
- `src/flows/<domain>`：流程对象
- `tests/<domain>`：测试用例
- `src/data/testdata/`：测试数据

## 扩展要求

- 不允许只增加测试用例，不补页面或流程抽象
- 公共复杂控件优先复用 `components/`
- 跨系统逻辑优先放到 `flows/cross_system/`
- 公共断言优先沉淀到断言助手或领域服务