"""
Application settings and configuration
"""

import os
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Telegram Configuration
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    bot_username: Optional[str] = Field(None, env="BOT_USERNAME")
    webhook_url: Optional[str] = Field(None, env="WEBHOOK_URL")
    
    # Mailsac Configuration
    mailsac_api_key: str = Field(..., env="MAILSAC_API_KEY")
    mailsac_base_url: str = Field("https://mailsac.com/api", env="MAILSAC_BASE_URL")
    
    # Google Gemini Configuration
    google_ai_api_key: str = Field(..., env="GOOGLE_AI_API_KEY")
    gemini_model: str = Field("gemini-pro", env="GEMINI_MODEL")
    
    # Bot Configuration
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # Email Configuration
    default_email_domain: str = Field("mailsac.com", env="DEFAULT_EMAIL_DOMAIN")
    email_retention_hours: int = Field(24, env="EMAIL_RETENTION_HOURS")
    max_emails_per_user: int = Field(10, env="MAX_EMAILS_PER_USER")
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @validator("email_retention_hours")
    def validate_retention_hours(cls, v):
        """Validate email retention hours."""
        if v < 1 or v > 168:  # 1 hour to 1 week
            raise ValueError("Email retention must be between 1 and 168 hours")
        return v
    
    @validator("max_emails_per_user")
    def validate_max_emails(cls, v):
        """Validate max emails per user."""
        if v < 1 or v > 100:
            raise ValueError("Max emails per user must be between 1 and 100")
        return v
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False