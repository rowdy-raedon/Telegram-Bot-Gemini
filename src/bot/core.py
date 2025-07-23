"""
Core Telegram Bot implementation
"""

import logging
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src.config.settings import Settings
from src.bot.handlers import setup_handlers
from src.bot.middleware import setup_middleware
from src.services.mailsac import MailsacService
from src.services.gemini import GeminiService


class TelegramBot:
    """Main Telegram Bot class."""
    
    def __init__(self, settings: Settings):
        """Initialize the bot."""
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        # Initialize bot and dispatcher
        self.bot = Bot(
            token=settings.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher()
        
        # Initialize services
        self.mailsac_service = MailsacService(
            api_key=settings.mailsac_api_key,
            base_url=settings.mailsac_base_url
        )
        self.gemini_service = GeminiService(
            api_key=settings.google_ai_api_key,
            model=settings.gemini_model
        )
        
        # Setup middleware and handlers
        setup_middleware(self.dp, self.mailsac_service, self.gemini_service)
        setup_handlers(self.dp)
        
        self.logger.info("✅ Bot initialized successfully")
    
    async def start_polling(self) -> None:
        """Start bot in polling mode."""
        self.logger.info("🔄 Starting bot in polling mode...")
        await self.dp.start_polling(self.bot)
    
    async def start_webhook(self, webhook_url: str) -> None:
        """Start bot in webhook mode."""
        if not webhook_url:
            raise ValueError("Webhook URL is required for webhook mode")
        
        self.logger.info(f"🌐 Starting bot in webhook mode: {webhook_url}")
        
        # Create webhook handler
        webhook_handler = SimpleRequestHandler(
            dispatcher=self.dp,
            bot=self.bot
        )
        
        # Create web application
        app = web.Application()
        webhook_handler.register(app, path="/webhook")
        setup_application(app, self.dp, bot=self.bot)
        
        # Set webhook
        await self.bot.set_webhook(webhook_url)
        
        # Start web server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8000)
        await site.start()
        
        self.logger.info("🚀 Webhook server started on port 8000")
        
        # Keep running
        import asyncio
        await asyncio.Event().wait()
    
    async def shutdown(self) -> None:
        """Shutdown the bot gracefully."""
        self.logger.info("🛑 Shutting down bot...")
        await self.bot.session.close()
        self.logger.info("✅ Bot shutdown complete")