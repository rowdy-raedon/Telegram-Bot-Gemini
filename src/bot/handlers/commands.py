"""
Command handlers for the bot
"""

import logging
from typing import Any

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode

from src.bot.keyboards.inline import get_main_menu_keyboard, get_email_actions_keyboard
from src.services.mailsac import MailsacService
from src.services.gemini import GeminiService
from src.bot.utils.email import generate_random_email, format_email_list

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, mailsac_service: MailsacService) -> None:
    """Handle /start command."""
    welcome_text = f"""
🤖 {hbold('Welcome to Advanced Temp Email Bot!')}

🚀 {hbold('Features:')}
• 📧 Generate temporary emails instantly
• 🤖 AI-powered email analysis with Gemini
• 📬 Real-time inbox monitoring
• 🔒 Privacy-first approach

🎯 {hbold('Quick Actions:')}
Use the buttons below or try these commands:
• {hcode('/new_email')} - Create new temp email
• {hcode('/inbox')} - View current inbox
• {hcode('/help')} - Show all commands
    """
    
    keyboard = get_main_menu_keyboard()
    await message.answer(welcome_text, reply_markup=keyboard)


@router.message(Command("new_email"))
async def new_email_handler(message: Message, mailsac_service: MailsacService) -> None:
    """Handle /new_email command."""
    try:
        # Generate random email
        email_address = generate_random_email()
        
        # Store in user context (you might want to use proper storage)
        # For now, we'll just show the email
        
        response_text = f"""
📧 {hbold('New Temporary Email Created!')}

{hcode(email_address)}

🔄 This email is ready to receive messages
📬 Use {hcode('/inbox')} to check for new emails
⏱️ Emails auto-delete after 24 hours

💡 {hbold('Pro tip:')} You can use AI to analyze emails!
        """
        
        keyboard = get_email_actions_keyboard(email_address)
        await message.answer(response_text, reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Error creating new email: {e}")
        await message.answer("❌ Failed to create new email. Please try again.")


@router.message(Command("inbox"))
async def inbox_handler(message: Message, mailsac_service: MailsacService) -> None:
    """Handle /inbox command."""
    # TODO: Get user's current email from storage
    email_address = "user@mailsac.com"  # Placeholder
    
    try:
        messages = await mailsac_service.get_messages(email_address)
        
        if not messages:
            await message.answer("📭 Your inbox is empty!")
            return
        
        response_text = f"📬 {hbold('Inbox for')} {hcode(email_address)}\\n\\n"
        response_text += format_email_list(messages)
        
        await message.answer(response_text)
        
    except Exception as e:
        logger.error(f"Error fetching inbox: {e}")
        await message.answer("❌ Failed to fetch inbox. Please try again.")


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Handle /help command."""
    help_text = f"""
🤖 {hbold('Advanced Temp Email Bot - Commands')}

📧 {hbold('Email Management:')}
• {hcode('/start')} - Show welcome message and main menu
• {hcode('/new_email')} - Generate new temporary email
• {hcode('/inbox')} - View current inbox
• {hcode('/read <id>')} - Read specific email
• {hcode('/delete <id>')} - Delete specific email
• {hcode('/clear')} - Clear all emails

🤖 {hbold('AI Features:')}
• {hcode('/summarize <id>')} - Get AI summary of email
• {hcode('/ask <id> <question>')} - Ask AI about email content
• {hcode('/analyze <id>')} - Analyze email for spam/phishing

⚙️ {hbold('Settings:')}
• {hcode('/settings')} - Configure bot preferences
• {hcode('/stats')} - View usage statistics

❓ {hbold('Need Help?')}
Contact support or check our documentation for more details.
    """
    
    await message.answer(help_text)


@router.message(Command("settings"))
async def settings_handler(message: Message) -> None:
    """Handle /settings command."""
    # TODO: Implement settings management
    await message.answer("⚙️ Settings panel coming soon!")


def register_command_handlers(dp: Any) -> None:
    """Register command handlers."""
    dp.include_router(router)