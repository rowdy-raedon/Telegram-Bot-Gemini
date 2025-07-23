"""
Email utility functions
"""

import random
import string
from typing import List, Dict, Any
from datetime import datetime

from aiogram.utils.markdown import hcode, hbold


def generate_random_email(domain: str = "mailsac.com") -> str:
    """Generate a random email address."""
    # Generate random username with mix of letters and numbers
    username_length = random.randint(8, 12)
    username = ''.join(
        random.choices(
            string.ascii_lowercase + string.digits, 
            k=username_length
        )
    )
    
    return f"{username}@{domain}"


def format_email_list(messages: List[Dict[str, Any]], max_messages: int = 10) -> str:
    """Format list of email messages for display."""
    if not messages:
        return "📭 No messages found"
    
    formatted_messages = []
    
    for i, msg in enumerate(messages[:max_messages]):
        # Extract message details
        msg_id = msg.get('id', 'N/A')[:8]
        sender = msg.get('from_address', 'Unknown')
        subject = msg.get('subject', 'No Subject')
        received = msg.get('received', datetime.now())
        
        # Truncate long subjects
        if len(subject) > 40:
            subject = subject[:37] + "..."
        
        # Truncate long sender addresses
        if len(sender) > 30:
            sender = sender[:27] + "..."
        
        # Format timestamp
        if isinstance(received, datetime):
            time_str = received.strftime("%m/%d %H:%M")
        else:
            time_str = "Unknown"
        
        # Create formatted message entry
        formatted_msg = f"""
{hbold(f'{i+1}.')} {hcode(msg_id)}
📨 {sender}
📝 {subject}
🕐 {time_str}
        """
        formatted_messages.append(formatted_msg.strip())
    
    result = "\n\n".join(formatted_messages)
    
    if len(messages) > max_messages:
        result += f"\n\n... and {len(messages) - max_messages} more messages"
    
    return result


def format_email_content(message: Dict[str, Any]) -> str:
    """Format email content for display."""
    sender = message.get('from_address', 'Unknown')
    subject = message.get('subject', 'No Subject')
    received = message.get('received', datetime.now())
    body = message.get('body', 'No content available')
    
    # Format timestamp
    if isinstance(received, datetime):
        time_str = received.strftime("%B %d, %Y at %H:%M")
    else:
        time_str = "Unknown time"
    
    # Truncate very long body content
    if len(body) > 2000:
        body = body[:1997] + "..."
    
    formatted_content = f"""
{hbold('From:')} {sender}
{hbold('Subject:')} {subject}
{hbold('Received:')} {time_str}

{hbold('Content:')}
{body}
    """
    
    return formatted_content.strip()


def extract_plain_text(html_content: str) -> str:
    """Extract plain text from HTML email content."""
    if not html_content:
        return "No content available"
    
    # Simple HTML tag removal (in production, use proper HTML parser)
    import re
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    
    # Decode common HTML entities
    html_entities = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&nbsp;': ' '
    }
    
    for entity, char in html_entities.items():
        text = text.replace(entity, char)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text or "No readable content"


def validate_email_address(email: str) -> bool:
    """Validate email address format."""
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_timestamp(timestamp: Any) -> str:
    """Format timestamp for display."""
    if isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%m/%d %H:%M")
        except (ValueError, AttributeError):
            return "Unknown"
    elif isinstance(timestamp, datetime):
        return timestamp.strftime("%m/%d %H:%M")
    else:
        return "Unknown"