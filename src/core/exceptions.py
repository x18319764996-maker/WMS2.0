"""自定义异常类型，用于区分配置错误和运行时跳过等特殊控制流。"""


class ConfigurationError(RuntimeError):
    """必需的配置项缺失或值非法时抛出。"""


class LiveExecutionSkipped(RuntimeError):
    """真实 UI 执行被主动跳过时抛出（如 ENABLE_LIVE_UI=false）。"""