"""Logging utilities"""
import logging
from typing import Any

class CustomLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def info(self, message: str, extra: dict[str, Any] | None = None):
        self.logger.info(message, extra=extra)

    def error(self, message: str, exc_info: bool = True, extra: dict[str, Any] | None = None):
        self.logger.error(message, exc_info=exc_info, extra=extra)

    def warning(self, message: str, extra: dict[str, Any] | None = None):
        self.logger.warning(message, extra=extra)

    def debug(self, message: str, extra: dict[str, Any] | None = None):
        self.logger.debug(message, extra=extra)

# Create loggers
request_logger = CustomLogger("app.requests")
auth_logger = CustomLogger("app.auth")
db_logger = CustomLogger("app.database")