"""中文说明：本文件是项目中的 Python 模块，用于承载对应的自动化能力或测试逻辑。"""

class ConfigurationError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


class LiveExecutionSkipped(RuntimeError):
    """Raised when live UI execution is intentionally skipped."""