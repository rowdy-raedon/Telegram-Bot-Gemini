#!/usr/bin/env python3
"""
Advanced Telegram Temp Email Bot
Main application entry point
"""

import asyncio
import argparse
import logging
from typing import Optional

from src.config.settings import Settings
from src.config.logging import setup_logging
from src.bot.core import TelegramBot


async def main(webhook: bool = False, webhook_url: Optional[str] = None) -> None:
    """Main application entry point."""
    # Load settings
    settings = Settings()
    
    # Setup logging
    setup_logging(settings.log_level, settings.debug)
    logger = logging.getLogger(__name__)
    
    logger.info("🤖 Starting Advanced Telegram Temp Email Bot")
    logger.info(f"📊 Debug mode: {settings.debug}")
    logger.info(f"🌐 Webhook mode: {webhook}")
    
    # Initialize and start bot
    bot = TelegramBot(settings)
    
    try:
        if webhook:
            await bot.start_webhook(webhook_url or settings.webhook_url)
        else:
            await bot.start_polling()
    except KeyboardInterrupt:
        logger.info("👋 Shutting down bot...")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        raise
    finally:
        await bot.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Telegram Temp Email Bot")
    parser.add_argument(
        "--webhook", 
        action="store_true", 
        help="Run in webhook mode instead of polling"
    )
    parser.add_argument(
        "--webhook-url", 
        type=str, 
        help="Webhook URL (overrides environment variable)"
    )
    
    args = parser.parse_args()
    
    # Run the bot
    asyncio.run(main(webhook=args.webhook, webhook_url=args.webhook_url))