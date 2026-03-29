<!-- 中文说明：本文件说明如何按规范新增测试用例与模板文件。 -->
# 新增用例模板说明

新增 UI 自动化用例时，请遵循以下顺序：

1. 明确业务域：OMS / WMS / CrossSystem
2. 如果需要新页面，先补页面对象
3. 如果是复杂流程，先补 Flow
4. 准备测试数据文件
5. 编写测试用例，只表达业务意图和断言

## 推荐模板

- 页面对象模板：`src/templates/page_template.py`
- 流程模板：`src/templates/flow_template.py`
- 用例模板：`src/templates/test_template.py`