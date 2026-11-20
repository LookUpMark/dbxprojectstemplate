"""Logging configuration for the project package.

Centralized loguru setup: import :func:`configure_logging` at the start of
every task or job entry point. One responsibility only — format, level, sink.
"""

import sys

from loguru import logger

# Message format: time, level, module origin, message.
_LOG_FORMAT = "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {name}:{function} - {message}"


def configure_logging(level: str = "INFO") -> None:
    """Configure the loguru sink and level for the current process.

    Args:
        level: Minimum severity to emit, e.g. ``"INFO"`` or ``"DEBUG"``.
    """
    logger.remove()
    logger.add(sys.stderr, level=level.upper(), format=_LOG_FORMAT)
