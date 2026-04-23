<!-- 中文说明：本文件说明如何扩展新的业务域并保持目录与分层一致。 -->
# 业务域扩展规范

## 目录规则

每新增一个业务域，必须同时考虑以下层级：

- `src/domains/<domain>`：领域模型、上下文、业务约束
- `src/pages/<domain>`：页面对象
- `src/flows/<domain>`：流程对象
- `tests/<domain>`：测试用例
- `src/data/testdata/`：测试数据

## 现有业务域参考

以 WMS 域为例，当前目录结构：

```
src/domains/wms/
    __init__.py          # WMS 领域子包
    models.py            # InventoryRecord 等数据模型
src/pages/wms/
    __init__.py          # WMS 页面对象子包
    login_page.py        # 登录页
    inbound_page.py      # 入库页
    outbound_page.py     # 出库页
    inventory_page.py    # 库存查询页
    customer_profile_page.py  # 客户档案页
src/flows/wms/
    __init__.py          # WMS 业务流子包
    warehouse_flow.py    # 入库→库存→出库完整作业链路
tests/wms/
    __init__.py          # WMS 测试子包
    test_login.py        # 登录功能测试
    test_inventory_flow.py  # 仓储作业流程测试
```

新增域（如 TMS 运输管理）时，需同步创建上述 5 层目录并保持相同结构。

## 扩展要求

- 不允许只增加测试用例，不补页面或流程抽象
- 公共复杂控件优先复用 `components/`
- 跨系统逻辑优先放到 `flows/cross_system/`
- 公共断言优先沉淀到断言助手或领域服务
- 新增文件必须遵循中文注解规范（见 `docs/case_template.md`）