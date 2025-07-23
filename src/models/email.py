"""
Email data models
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class EmailAttachment(BaseModel):
    """Email attachment model."""
    filename: str
    content_type: str
    size: int
    download_url: Optional[str] = None


class EmailMessage(BaseModel):
    """Email message model."""
    id: str = Field(..., description="Unique message identifier")
    from_address: str = Field(..., description="Sender email address")
    to_address: str = Field(..., description="Recipient email address")
    subject: str = Field(default="No Subject", description="Email subject")
    body: Optional[str] = Field(None, description="Email body content")
    received: datetime = Field(..., description="When email was received")
    attachments: List[EmailAttachment] = Field(default_factory=list)
    
    # AI analysis fields
    category: Optional[str] = None
    security_level: Optional[str] = None
    summary: Optional[str] = None
    
    @validator('from_address', 'to_address')
    def validate_email_format(cls, v):
        """Validate email address format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError(f"Invalid email format: {v}")
        return v
    
    @validator('body')
    def clean_body_content(cls, v):
        """Clean body content."""
        if v:
            # Remove excessive whitespace
            import re
            v = re.sub(r'\s+', ' ', v.strip())
        return v
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }