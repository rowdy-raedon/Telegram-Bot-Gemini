"""
Bot middleware package
"""

from aiogram import Dispatcher

from .services import ServicesMiddleware


def setup_middleware(dp: Dispatcher, mailsac_service, gemini_service) -> None:
    """Setup all middleware."""
    dp.middleware.setup(ServicesMiddleware(mailsac_service, gemini_service))