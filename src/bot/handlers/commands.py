"""
Command handlers for the bot
"""

import logging
from typing import Any, Optional

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hcode

from src.bot.keyboards.inline import get_main_menu_keyboard, get_email_actions_keyboard
from src.services.mailsac import MailsacService
from src.services.gemini import GeminiService
from src.bot.utils.email import generate_random_email, format_email_list
from src.bot.utils.validation import (
    validate_message_id, 
    validate_question, 
    validate_command_args,
    sanitize_input
)
from src.config.constants import BotMessages, LogConstants
from src.config.exceptions import BotException, ValidationError, EmailError, AIError, RateLimitError
from src.bot.utils.rate_limiter import check_rate_limits

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, mailsac_service: MailsacService) -> None:
    """Handle /start command."""
    try:
        # Log user action
        logger.info(
            LogConstants.USER_ACTION.format(
                user_id=message.from_user.id,
                action="start"
            )
        )
        
        keyboard = get_main_menu_keyboard()
        await message.answer(BotMessages.WELCOME_MESSAGE, reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await message.answer(BotMessages.ERROR_GENERIC)


@router.message(Command("new_email"))
async def new_email_handler(message: Message, mailsac_service: MailsacService) -> None:
    """Handle /new_email command."""
    try:
        # Check rate limits
        check_rate_limits(message.from_user.id, "mailsac")
        
        # Log user action
        logger.info(
            LogConstants.USER_ACTION.format(
                user_id=message.from_user.id,
                action="new_email"
            )
        )
        
        # Generate random email
        email_address = generate_random_email()
        
        # TODO: Store in user context with proper storage
        # For now, we'll just show the email
        
        response_text = BotMessages.EMAIL_CREATED.format(email_address=email_address)
        keyboard = get_email_actions_keyboard(email_address)
        
        await message.answer(response_text, reply_markup=keyboard)
        
        logger.info(f"Generated email {email_address} for user {message.from_user.id}")
        
    except RateLimitError as e:
        logger.warning(f"Rate limit error in new_email handler: {e}")
        await message.answer(e.user_message)
    except BotException as e:
        logger.error(f"Bot error in new_email handler: {e}")
        await message.answer(e.user_message)
    except Exception as e:
        logger.error(f"Unexpected error in new_email handler: {e}")
        await message.answer(BotMessages.ERROR_EMAIL_CREATION)


@router.message(Command("inbox"))
async def inbox_handler(message: Message, mailsac_service: MailsacService) -> None:
    """Handle /inbox command."""
    try:
        # Check rate limits
        check_rate_limits(message.from_user.id, "mailsac")
        
        # Log user action
        logger.info(
            LogConstants.USER_ACTION.format(
                user_id=message.from_user.id,
                action="inbox"
            )
        )
        
        # TODO: Get user's current email from storage
        email_address = "user@mailsac.com"  # Placeholder
        
        messages = await mailsac_service.get_messages(email_address)
        
        if not messages:
            await message.answer(BotMessages.INBOX_EMPTY)
            return
        
        response_text = BotMessages.INBOX_HEADER.format(email_address=email_address)
        response_text += format_email_list(messages)
        
        await message.answer(response_text)
        
        logger.info(f"Fetched {len(messages)} messages for user {message.from_user.id}")
        
    except EmailError as e:
        logger.error(f"Email error in inbox handler: {e}")
        await message.answer(e.user_message)
    except BotException as e:
        logger.error(f"Bot error in inbox handler: {e}")
        await message.answer(e.user_message)
    except Exception as e:
        logger.error(f"Unexpected error in inbox handler: {e}")
        await message.answer(BotMessages.ERROR_INBOX_FETCH)


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Handle /help command."""
    try:
        # Log user action
        logger.info(
            LogConstants.USER_ACTION.format(
                user_id=message.from_user.id,
                action="help"
            )
        )
        
        await message.answer(BotMessages.HELP_MESSAGE)
        
    except Exception as e:
        logger.error(f"Error in help handler: {e}")
        await message.answer(BotMessages.ERROR_GENERIC)


@router.message(Command("settings"))
async def settings_handler(message: Message) -> None:
    """Handle /settings command."""
    try:
        # Log user action
        logger.info(
            LogConstants.USER_ACTION.format(
                user_id=message.from_user.id,
                action="settings"
            )
        )
        
        # TODO: Implement settings management
        await message.answer(BotMessages.SETTINGS_COMING_SOON)
        
    except Exception as e:
        logger.error(f"Error in settings handler: {e}")
        await message.answer(BotMessages.ERROR_GENERIC)


@router.message(Command("read"))
async def read_handler(message: Message, mailsac_service: MailsacService) -> None:
    """Handle /read <message_id> command."""
    try:
        # Log user action
        logger.info(
            LogConstants.USER_ACTION.format(
                user_id=message.from_user.id,
                action="read"
            )
        )
        
        # Parse command arguments
        command_text = message.text or ""
        args = command_text.split()[1:]  # Remove command itself
        
        if not args:
            await message.answer("❌ Usage: /read <message_id>")
            return
        
        # Validate message ID
        message_id = validate_message_id(args[0])
        
        # TODO: Get user's current email from storage
        email_address = "user@mailsac.com"  # Placeholder
        
        # Fetch message content
        email_message = await mailsac_service.get_message_content(email_address, message_id)
        
        if not email_message:
            await message.answer("❌ Email not found. Please check the message ID.")
            return
        
        # Format and send message content
        response_text = f"""
📧 **From:** {email_message.from_address}
📝 **Subject:** {email_message.subject}
🕐 **Date:** {email_message.received.strftime('%Y-%m-%d %H:%M')}

**Content:**
{email_message.body or 'No content available'}
        """
        
        await message.answer(response_text)
        
        logger.info(f"User {message.from_user.id} read message {message_id}")
        
    except ValidationError as e:
        logger.warning(f"Validation error in read handler: {e}")
        await message.answer(e.user_message)
    except EmailError as e:
        logger.error(f"Email error in read handler: {e}")
        await message.answer(e.user_message)
    except BotException as e:
        logger.error(f"Bot error in read handler: {e}")
        await message.answer(e.user_message)
    except Exception as e:
        logger.error(f"Unexpected error in read handler: {e}")
        await message.answer(BotMessages.ERROR_GENERIC)


@router.message(Command("summarize"))
async def summarize_handler(message: Message, gemini_service: GeminiService, mailsac_service: MailsacService) -> None:
    """Handle /summarize <message_id> command."""
    try:
        # Log user action
        logger.info(
            LogConstants.USER_ACTION.format(
                user_id=message.from_user.id,
                action="summarize"
            )
        )
        
        # Parse command arguments
        command_text = message.text or ""
        args = command_text.split()[1:]
        
        if not args:
            await message.answer("❌ Usage: /summarize <message_id>")
            return
        
        # Validate message ID
        message_id = validate_message_id(args[0])
        
        # TODO: Get user's current email from storage
        email_address = "user@mailsac.com"  # Placeholder
        
        # Show processing message
        processing_msg = await message.answer(BotMessages.AI_SUMMARIZING)
        
        # Fetch message content
        email_message = await mailsac_service.get_message_content(email_address, message_id)
        
        if not email_message:
            await processing_msg.edit_text("❌ Email not found. Please check the message ID.")
            return
        
        # Generate AI summary
        email_content = f"Subject: {email_message.subject}\n\nContent: {email_message.body or 'No content'}"
        summary = await gemini_service.summarize_email(email_content)
        
        response_text = f"""
📝 **AI Summary**

**Email:** {message_id}
**Subject:** {email_message.subject}

**Summary:**
{summary}
        """
        
        await processing_msg.edit_text(response_text)
        
        logger.info(f"User {message.from_user.id} summarized message {message_id}")
        
    except ValidationError as e:
        logger.warning(f"Validation error in summarize handler: {e}")
        await message.answer(e.user_message)
    except AIError as e:
        logger.error(f"AI error in summarize handler: {e}")
        await message.answer(e.user_message)
    except EmailError as e:
        logger.error(f"Email error in summarize handler: {e}")
        await message.answer(e.user_message)
    except BotException as e:
        logger.error(f"Bot error in summarize handler: {e}")
        await message.answer(e.user_message)
    except Exception as e:
        logger.error(f"Unexpected error in summarize handler: {e}")
        await message.answer(BotMessages.AI_ERROR)


@router.message(Command("ask"))
async def ask_handler(message: Message, gemini_service: GeminiService, mailsac_service: MailsacService) -> None:
    """Handle /ask <message_id> <question> command."""
    try:
        # Log user action
        logger.info(
            LogConstants.USER_ACTION.format(
                user_id=message.from_user.id,
                action="ask"
            )
        )
        
        # Parse command arguments
        command_text = message.text or ""
        parts = command_text.split(maxsplit=2)  # Split into command, message_id, question
        
        if len(parts) < 3:
            await message.answer("❌ Usage: /ask <message_id> <question>")
            return
        
        # Validate inputs
        message_id = validate_message_id(parts[1])
        question = validate_question(parts[2])
        
        # TODO: Get user's current email from storage
        email_address = "user@mailsac.com"  # Placeholder
        
        # Show processing message
        processing_msg = await message.answer(BotMessages.AI_THINKING)
        
        # Fetch message content
        email_message = await mailsac_service.get_message_content(email_address, message_id)
        
        if not email_message:
            await processing_msg.edit_text("❌ Email not found. Please check the message ID.")
            return
        
        # Generate AI response
        email_content = f"Subject: {email_message.subject}\n\nContent: {email_message.body or 'No content'}"
        answer = await gemini_service.answer_question_about_email(email_content, question)
        
        response_text = f"""
🤖 **AI Answer**

**Question:** {question}
**Email:** {message_id}

**Answer:**
{answer}
        """
        
        await processing_msg.edit_text(response_text)
        
        logger.info(f"User {message.from_user.id} asked about message {message_id}")
        
    except ValidationError as e:
        logger.warning(f"Validation error in ask handler: {e}")
        await message.answer(e.user_message)
    except AIError as e:
        logger.error(f"AI error in ask handler: {e}")
        await message.answer(e.user_message)
    except EmailError as e:
        logger.error(f"Email error in ask handler: {e}")
        await message.answer(e.user_message)
    except BotException as e:
        logger.error(f"Bot error in ask handler: {e}")
        await message.answer(e.user_message)
    except Exception as e:
        logger.error(f"Unexpected error in ask handler: {e}")
        await message.answer(BotMessages.AI_ERROR)


def register_command_handlers(dp: Any) -> None:
    """Register command handlers."""
    dp.include_router(router)