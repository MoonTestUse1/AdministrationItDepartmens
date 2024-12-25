"""Handlers initialization"""
from .callbacks import router as callbacks_router
from .start import router as start_router
from .callbacks import get_updated_keyboard

__all__ = ['callbacks_router', 'start_router', 'get_updated_keyboard']