"""
Callback query handlers for inline keyboards
"""

import logging
from typing import Any

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold, hcode

from src.bot.keyboards.inline import get_main_menu_keyboard
from src.services.mailsac import MailsacService
from src.services.gemini import GeminiService
from src.bot.utils.email import generate_random_email

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "new_email")
async def new_email_callback(callback: CallbackQuery, mailsac_service: MailsacService) -> None:
    """Handle new email creation via callback."""
    try:
        email_address = generate_random_email()
        
        response_text = f"""
📧 {hbold('New Email Created!')}

{hcode(email_address)}

Ready to receive messages! ✅
        """
        
        await callback.message.edit_text(response_text, reply_markup=get_main_menu_keyboard())
        await callback.answer("✅ New email created!")
        
    except Exception as e:
        logger.error(f"Error in new_email_callback: {e}")
        await callback.answer("❌ Failed to create email", show_alert=True)


@router.callback_query(F.data == "view_inbox")
async def view_inbox_callback(callback: CallbackQuery, mailsac_service: MailsacService) -> None:
    """Handle inbox viewing via callback."""
    try:
        # TODO: Get user's current email from storage
        email_address = "user@mailsac.com"  # Placeholder
        
        messages = await mailsac_service.get_messages(email_address)
        
        if not messages:
            await callback.answer("📭 Inbox is empty!", show_alert=True)
            return
        
        response_text = f"📬 {hbold('You have')} {len(messages)} {hbold('messages')}"
        await callback.message.edit_text(response_text, reply_markup=get_main_menu_keyboard())
        await callback.answer(f"📬 {len(messages)} messages found")
        
    except Exception as e:
        logger.error(f"Error in view_inbox_callback: {e}")
        await callback.answer("❌ Failed to load inbox", show_alert=True)


@router.callback_query(F.data == "ai_features")
async def ai_features_callback(callback: CallbackQuery) -> None:
    """Handle AI features menu."""
    response_text = f"""
🤖 {hbold('AI Features')}

🧠 Available AI capabilities:
• 📝 Email summarization
• ❓ Content Q&A
• 🛡️ Spam/phishing detection
• 🌐 Multi-language support
• 📊 Content analysis

💡 {hbold('How to use:')}
Select an email and choose an AI action!
    """
    
    await callback.message.edit_text(response_text, reply_markup=get_main_menu_keyboard())
    await callback.answer("🤖 AI features ready!")


@router.callback_query(F.data == "settings")
async def settings_callback(callback: CallbackQuery) -> None:
    """Handle settings menu."""
    response_text = f"""
⚙️ {hbold('Bot Settings')}

🔧 Configuration options:
• 🔔 Notification preferences
• 🗑️ Auto-delete settings
• 🌐 Language selection
• 📊 Privacy controls

⏱️ Coming soon in next update!
    """
    
    await callback.message.edit_text(response_text, reply_markup=get_main_menu_keyboard())
    await callback.answer("⚙️ Settings panel")


@router.callback_query(F.data == "back_to_main")
async def back_to_main_callback(callback: CallbackQuery) -> None:
    """Handle back to main menu."""
    welcome_text = """
🤖 Welcome back to Advanced Temp Email Bot!

Choose an action from the menu below:
    """
    
    await callback.message.edit_text(welcome_text, reply_markup=get_main_menu_keyboard())
    await callback.answer()


def register_callback_handlers(dp: Any) -> None:
    """Register callback handlers."""
    dp.include_router(router)