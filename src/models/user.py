"""
User data models and settings
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class NotificationLevel(str, Enum):
    """Notification level options."""
    ALL = "all"
    IMPORTANT = "important"
    NONE = "none"


class LanguageCode(str, Enum):
    """Supported language codes."""
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    IT = "it"
    PT = "pt"
    RU = "ru"
    ZH = "zh"
    JA = "ja"
    KO = "ko"


class UserSettings(BaseModel):
    """User settings and preferences."""
    # Notification settings
    notification_level: NotificationLevel = NotificationLevel.ALL
    notify_new_emails: bool = True
    notify_ai_analysis: bool = True
    
    # Auto-deletion settings
    auto_delete_enabled: bool = True
    auto_delete_hours: int = Field(default=24, ge=1, le=168)  # 1 hour to 1 week
    
    # Language and localization
    language: LanguageCode = LanguageCode.EN
    timezone: Optional[str] = None
    
    # Privacy settings
    store_email_content: bool = False
    share_usage_analytics: bool = True
    
    # AI settings
    ai_analysis_enabled: bool = True
    ai_security_check: bool = True
    ai_auto_categorize: bool = True
    
    class Config:
        """Pydantic config."""
        use_enum_values = True


class UserSession(BaseModel):
    """User session data."""
    user_id: int = Field(..., description="Telegram user ID")
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    # Current session data
    current_email: Optional[str] = None
    active_emails: List[str] = Field(default_factory=list)
    
    # Session tracking
    first_seen: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    message_count: int = 0
    
    # User settings
    settings: UserSettings = Field(default_factory=UserSettings)
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
        self.message_count += 1
    
    def add_email(self, email_address: str) -> None:
        """Add email to active emails list."""
        if email_address not in self.active_emails:
            self.active_emails.append(email_address)
        self.current_email = email_address
    
    def remove_email(self, email_address: str) -> None:
        """Remove email from active emails list."""
        if email_address in self.active_emails:
            self.active_emails.remove(email_address)
        
        # Update current email if removed
        if self.current_email == email_address:
            self.current_email = self.active_emails[0] if self.active_emails else None
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserStatistics(BaseModel):
    """User usage statistics."""
    user_id: int
    
    # Email statistics
    emails_created: int = 0
    emails_received: int = 0
    emails_deleted: int = 0
    
    # AI usage statistics
    ai_summaries_generated: int = 0
    ai_questions_asked: int = 0
    ai_security_checks: int = 0
    ai_translations: int = 0
    
    # Session statistics
    total_sessions: int = 0
    total_time_active: int = 0  # seconds
    commands_used: Dict[str, int] = Field(default_factory=dict)
    
    # Timestamps
    first_use: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def increment_counter(self, counter_name: str, amount: int = 1) -> None:
        """Increment a statistics counter."""
        if hasattr(self, counter_name):
            setattr(self, counter_name, getattr(self, counter_name) + amount)
        self.last_updated = datetime.now()
    
    def increment_command(self, command: str) -> None:
        """Increment command usage counter."""
        self.commands_used[command] = self.commands_used.get(command, 0) + 1
        self.last_updated = datetime.now()
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }