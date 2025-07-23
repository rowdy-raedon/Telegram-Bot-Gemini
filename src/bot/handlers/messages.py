"""
Message handlers for non-command messages
"""

import logging
from typing import Any

from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from src.services.gemini import GeminiService

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text)
async def text_message_handler(message: Message, gemini_service: GeminiService) -> None:
    """Handle regular text messages with AI assistance."""
    try:
        # Check if message looks like a question or request for help
        text = message.text.lower()
        
        if any(word in text for word in ['help', 'how', 'what', 'email', 'temp', 'temporary']):
            # Provide helpful response about bot capabilities
            response = f"""
🤖 {hbold('I can help you with temporary emails!')}

📧 {hbold('Quick commands:')}
• /new_email - Create a new temporary email
• /inbox - Check your current inbox
• /help - See all available commands

💡 You can also ask me questions about emails using AI!
            """
            await message.answer(response)
        else:
            # For other messages, suggest using commands
            await message.answer(
                "👋 Hi! Use /start to see the main menu or /help for all commands."
            )
            
    except Exception as e:
        logger.error(f"Error handling text message: {e}")
        await message.answer("❌ Something went wrong. Please try again.")


def register_message_handlers(dp: Any) -> None:
    """Register message handlers."""
    dp.include_router(router)