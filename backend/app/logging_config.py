"""Logging configuration for the application"""
import sys

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": sys.stdout
        }
    },
    "loggers": {
        "": {  # Root logger
            "handlers": ["console"],
            "level": "INFO"
        },
        "app": {  # Application logger
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "app.access": {  # Access logger
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        }
    }
}