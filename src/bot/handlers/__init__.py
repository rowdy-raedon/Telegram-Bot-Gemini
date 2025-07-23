"""
Bot handlers package
"""

from aiogram import Dispatcher

from .commands import register_command_handlers
from .callbacks import register_callback_handlers
from .messages import register_message_handlers


def setup_handlers(dp: Dispatcher) -> None:
    """Setup all bot handlers."""
    register_command_handlers(dp)
    register_callback_handlers(dp)
    register_message_handlers(dp)