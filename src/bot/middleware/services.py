"""
Services middleware for dependency injection
"""

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.services.mailsac import MailsacService
from src.services.gemini import GeminiService


class ServicesMiddleware(BaseMiddleware):
    """Middleware to inject services into handlers."""
    
    def __init__(self, mailsac_service: MailsacService, gemini_service: GeminiService):
        """Initialize services middleware."""
        self.mailsac_service = mailsac_service
        self.gemini_service = gemini_service
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Inject services into handler data."""
        data["mailsac_service"] = self.mailsac_service
        data["gemini_service"] = self.gemini_service
        
        return await handler(event, data)