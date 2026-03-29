class ConfigurationError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


class LiveExecutionSkipped(RuntimeError):
    """Raised when live UI execution is intentionally skipped."""