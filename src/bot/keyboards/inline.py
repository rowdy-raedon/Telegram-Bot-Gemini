"""
Inline keyboard layouts
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Get main menu inline keyboard."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📧 New Email", callback_data="new_email"),
        InlineKeyboardButton(text="📬 View Inbox", callback_data="view_inbox")
    )
    builder.row(
        InlineKeyboardButton(text="🤖 AI Features", callback_data="ai_features"),
        InlineKeyboardButton(text="⚙️ Settings", callback_data="settings")
    )
    
    return builder.as_markup()


def get_email_actions_keyboard(email_address: str) -> InlineKeyboardMarkup:
    """Get email-specific actions keyboard."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📬 Check Inbox", callback_data=f"inbox_{email_address}"),
        InlineKeyboardButton(text="🗑️ Delete All", callback_data=f"delete_all_{email_address}")
    )
    builder.row(
        InlineKeyboardButton(text="🔄 New Email", callback_data="new_email"),
        InlineKeyboardButton(text="🏠 Main Menu", callback_data="back_to_main")
    )
    
    return builder.as_markup()


def get_message_actions_keyboard(message_id: str, email_address: str) -> InlineKeyboardMarkup:
    """Get message-specific actions keyboard."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text="📝 Summarize", 
            callback_data=f"summarize_{message_id}_{email_address}"
        ),
        InlineKeyboardButton(
            text="❓ Ask AI", 
            callback_data=f"ask_{message_id}_{email_address}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🛡️ Security Check", 
            callback_data=f"security_{message_id}_{email_address}"
        ),
        InlineKeyboardButton(
            text="🗑️ Delete", 
            callback_data=f"delete_{message_id}_{email_address}"
        )
    )
    builder.row(
        InlineKeyboardButton(text="📬 Back to Inbox", callback_data=f"inbox_{email_address}")
    )
    
    return builder.as_markup()


def get_ai_features_keyboard() -> InlineKeyboardMarkup:
    """Get AI features menu keyboard."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="📝 Summarize Email", callback_data="ai_summarize"),
        InlineKeyboardButton(text="❓ Ask Questions", callback_data="ai_ask")
    )
    builder.row(
        InlineKeyboardButton(text="🛡️ Security Analysis", callback_data="ai_security"),
        InlineKeyboardButton(text="🌐 Translate", callback_data="ai_translate")
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Back to Main", callback_data="back_to_main")
    )
    
    return builder.as_markup()


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Get settings menu keyboard."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="🔔 Notifications", callback_data="settings_notifications"),
        InlineKeyboardButton(text="🗑️ Auto-delete", callback_data="settings_delete")
    )
    builder.row(
        InlineKeyboardButton(text="🌐 Language", callback_data="settings_language"),
        InlineKeyboardButton(text="📊 Privacy", callback_data="settings_privacy")
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Back to Main", callback_data="back_to_main")
    )
    
    return builder.as_markup()


def get_confirmation_keyboard(action: str, item_id: str) -> InlineKeyboardMarkup:
    """Get confirmation keyboard for destructive actions."""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="✅ Confirm", callback_data=f"confirm_{action}_{item_id}"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_action")
    )
    
    return builder.as_markup()