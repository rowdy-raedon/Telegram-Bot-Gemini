"""
Custom exception classes for better error handling
"""

from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(Enum):
    """Error code enumeration."""
    
    # General errors
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    
    # API errors
    API_CONNECTION_ERROR = "API_CONNECTION_ERROR"
    API_TIMEOUT_ERROR = "API_TIMEOUT_ERROR"
    API_RATE_LIMIT_ERROR = "API_RATE_LIMIT_ERROR"
    API_UNAUTHORIZED_ERROR = "API_UNAUTHORIZED_ERROR"
    API_NOT_FOUND_ERROR = "API_NOT_FOUND_ERROR"
    API_SERVER_ERROR = "API_SERVER_ERROR"
    
    # Email errors
    EMAIL_INVALID_FORMAT = "EMAIL_INVALID_FORMAT"
    EMAIL_NOT_FOUND = "EMAIL_NOT_FOUND"
    EMAIL_CREATION_FAILED = "EMAIL_CREATION_FAILED"
    EMAIL_FETCH_FAILED = "EMAIL_FETCH_FAILED"
    EMAIL_DELETE_FAILED = "EMAIL_DELETE_FAILED"
    
    # AI errors
    AI_SERVICE_UNAVAILABLE = "AI_SERVICE_UNAVAILABLE"
    AI_INVALID_RESPONSE = "AI_INVALID_RESPONSE"
    AI_QUOTA_EXCEEDED = "AI_QUOTA_EXCEEDED"
    AI_CONTENT_FILTERED = "AI_CONTENT_FILTERED"
    
    # User errors
    USER_RATE_LIMIT_EXCEEDED = "USER_RATE_LIMIT_EXCEEDED"
    USER_INPUT_TOO_LONG = "USER_INPUT_TOO_LONG"
    USER_INVALID_COMMAND = "USER_INVALID_COMMAND"


class BotException(Exception):
    """Base exception class for the bot."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        user_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Initialize bot exception."""
        super().__init__(message)
        self.error_code = error_code
        self.user_message = user_message or "An error occurred. Please try again."
        self.details = details or {}
        self.original_message = message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary."""
        return {
            "error_code": self.error_code.value,
            "message": self.original_message,
            "user_message": self.user_message,
            "details": self.details
        }


class ValidationError(BotException):
    """Exception for input validation errors."""
    
    def __init__(self, field: str, value: Any, reason: str):
        """Initialize validation error."""
        message = f"Validation failed for field '{field}': {reason}"
        user_message = f"Invalid {field}. {reason}"
        details = {"field": field, "value": str(value), "reason": reason}
        
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            user_message=user_message,
            details=details
        )


class APIError(BotException):
    """Exception for API-related errors."""
    
    def __init__(
        self,
        service: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
        error_code: ErrorCode = ErrorCode.API_CONNECTION_ERROR
    ):
        """Initialize API error."""
        message = f"{service} API error"
        if status_code:
            message += f" (status: {status_code})"
        if response_text:
            message += f": {response_text}"
        
        user_message = f"{service} service is temporarily unavailable. Please try again later."
        details = {
            "service": service,
            "status_code": status_code,
            "response_text": response_text
        }
        
        super().__init__(
            message=message,
            error_code=error_code,
            user_message=user_message,
            details=details
        )


class EmailError(BotException):
    """Exception for email-related errors."""
    
    def __init__(
        self,
        operation: str,
        email_address: Optional[str] = None,
        reason: Optional[str] = None,
        error_code: ErrorCode = ErrorCode.EMAIL_FETCH_FAILED
    ):
        """Initialize email error."""
        message = f"Email {operation} failed"
        if email_address:
            message += f" for {email_address}"
        if reason:
            message += f": {reason}"
        
        user_message = f"Failed to {operation} email. Please try again."
        details = {
            "operation": operation,
            "email_address": email_address,
            "reason": reason
        }
        
        super().__init__(
            message=message,
            error_code=error_code,
            user_message=user_message,
            details=details
        )


class AIError(BotException):
    """Exception for AI service errors."""
    
    def __init__(
        self,
        operation: str,
        reason: Optional[str] = None,
        error_code: ErrorCode = ErrorCode.AI_SERVICE_UNAVAILABLE
    ):
        """Initialize AI error."""
        message = f"AI {operation} failed"
        if reason:
            message += f": {reason}"
        
        user_message = "AI service is currently unavailable. Please try again later."
        details = {
            "operation": operation,
            "reason": reason
        }
        
        super().__init__(
            message=message,
            error_code=error_code,
            user_message=user_message,
            details=details
        )


class RateLimitError(BotException):
    """Exception for rate limiting."""
    
    def __init__(self, limit_type: str, retry_after: Optional[int] = None):
        """Initialize rate limit error."""
        message = f"Rate limit exceeded: {limit_type}"
        user_message = "Too many requests. Please wait a moment before trying again."
        
        if retry_after:
            user_message += f" (retry in {retry_after} seconds)"
        
        details = {
            "limit_type": limit_type,
            "retry_after": retry_after
        }
        
        super().__init__(
            message=message,
            error_code=ErrorCode.USER_RATE_LIMIT_EXCEEDED,
            user_message=user_message,
            details=details
        )


class ConfigurationError(BotException):
    """Exception for configuration errors."""
    
    def __init__(self, setting: str, reason: str):
        """Initialize configuration error."""
        message = f"Configuration error for '{setting}': {reason}"
        user_message = "Bot configuration error. Please contact administrator."
        details = {"setting": setting, "reason": reason}
        
        super().__init__(
            message=message,
            error_code=ErrorCode.CONFIGURATION_ERROR,
            user_message=user_message,
            details=details
        )