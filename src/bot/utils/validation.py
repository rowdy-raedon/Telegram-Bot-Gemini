"""
Input validation and sanitization utilities
"""

import re
import html
from typing import Optional, Any

from src.config.constants import EmailConstants, SecurityConstants
from src.config.exceptions import ValidationError


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize user input by removing potentially dangerous content."""
    if not isinstance(text, str):
        raise ValidationError("input", text, "Input must be a string")
    
    # Remove HTML entities
    text = html.unescape(text)
    
    # Remove potentially dangerous patterns
    for pattern in SecurityConstants.BLOCKED_PATTERNS:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Keep only allowed characters
    text = re.sub(f'[^{SecurityConstants.ALLOWED_CHARS}]', '', text)
    
    # Limit length
    max_len = max_length or SecurityConstants.MAX_INPUT_LENGTH
    if len(text) > max_len:
        raise ValidationError("input", text, f"Input too long (max {max_len} characters)")
    
    return text.strip()


def validate_email_address(email: str) -> str:
    """Validate email address format."""
    if not isinstance(email, str):
        raise ValidationError("email", email, "Email must be a string")
    
    email = email.strip().lower()
    
    if not email:
        raise ValidationError("email", email, "Email cannot be empty")
    
    if len(email) > EmailConstants.MAX_EMAIL_LENGTH:
        raise ValidationError(
            "email", 
            email, 
            f"Email too long (max {EmailConstants.MAX_EMAIL_LENGTH} characters)"
        )
    
    if not re.match(EmailConstants.EMAIL_REGEX, email):
        raise ValidationError("email", email, "Invalid email format")
    
    return email


def validate_message_id(message_id: str) -> str:
    """Validate message ID format."""
    if not isinstance(message_id, str):
        raise ValidationError("message_id", message_id, "Message ID must be a string")
    
    message_id = message_id.strip()
    
    if not message_id:
        raise ValidationError("message_id", message_id, "Message ID cannot be empty")
    
    # Message IDs should be alphanumeric
    if not re.match(r'^[a-zA-Z0-9]+$', message_id):
        raise ValidationError("message_id", message_id, "Invalid message ID format")
    
    if len(message_id) < 8 or len(message_id) > 50:
        raise ValidationError(
            "message_id", 
            message_id, 
            "Message ID must be between 8 and 50 characters"
        )
    
    return message_id


def validate_question(question: str) -> str:
    """Validate AI question input."""
    if not isinstance(question, str):
        raise ValidationError("question", question, "Question must be a string")
    
    question = question.strip()
    
    if not question:
        raise ValidationError("question", question, "Question cannot be empty")
    
    if len(question) < 3:
        raise ValidationError("question", question, "Question too short (minimum 3 characters)")
    
    if len(question) > 500:
        raise ValidationError("question", question, "Question too long (maximum 500 characters)")
    
    # Remove potentially dangerous content
    question = sanitize_input(question, 500)
    
    return question


def validate_username(username: str) -> str:
    """Validate username for email generation."""
    if not isinstance(username, str):
        raise ValidationError("username", username, "Username must be a string")
    
    username = username.strip().lower()
    
    if not username:
        raise ValidationError("username", username, "Username cannot be empty")
    
    if len(username) < EmailConstants.MIN_USERNAME_LENGTH:
        raise ValidationError(
            "username", 
            username, 
            f"Username too short (minimum {EmailConstants.MIN_USERNAME_LENGTH} characters)"
        )
    
    if len(username) > EmailConstants.MAX_USERNAME_LENGTH:
        raise ValidationError(
            "username", 
            username, 
            f"Username too long (maximum {EmailConstants.MAX_USERNAME_LENGTH} characters)"
        )
    
    # Username should only contain letters, numbers, dots, and hyphens
    if not re.match(r'^[a-zA-Z0-9.-]+$', username):
        raise ValidationError(
            "username", 
            username, 
            "Username can only contain letters, numbers, dots, and hyphens"
        )
    
    # Cannot start or end with dot or hyphen
    if username.startswith(('.', '-')) or username.endswith(('.', '-')):
        raise ValidationError(
            "username", 
            username, 
            "Username cannot start or end with dot or hyphen"
        )
    
    return username


def validate_command_args(command: str, args: list, min_args: int = 0, max_args: Optional[int] = None) -> list:
    """Validate command arguments."""
    if not isinstance(args, list):
        raise ValidationError("args", args, "Arguments must be a list")
    
    if len(args) < min_args:
        raise ValidationError(
            "args", 
            args, 
            f"Command '{command}' requires at least {min_args} arguments"
        )
    
    if max_args is not None and len(args) > max_args:
        raise ValidationError(
            "args", 
            args, 
            f"Command '{command}' accepts maximum {max_args} arguments"
        )
    
    # Sanitize each argument
    sanitized_args = []
    for i, arg in enumerate(args):
        if not isinstance(arg, str):
            raise ValidationError(f"arg_{i}", arg, f"Argument {i} must be a string")
        
        sanitized_arg = sanitize_input(arg, 200)
        sanitized_args.append(sanitized_arg)
    
    return sanitized_args


def is_safe_content(content: str) -> bool:
    """Check if content is safe (doesn't contain malicious patterns)."""
    if not isinstance(content, str):
        return False
    
    # Check for blocked patterns
    for pattern in SecurityConstants.BLOCKED_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return False
    
    return True


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Safely truncate text to specified length."""
    if not isinstance(text, str):
        return str(text)[:max_length]
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    if not isinstance(text, str):
        return str(text)
    
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    return text.strip()


def extract_email_from_text(text: str) -> Optional[str]:
    """Extract email address from text."""
    if not isinstance(text, str):
        return None
    
    match = re.search(EmailConstants.EMAIL_REGEX, text)
    return match.group(0) if match else None