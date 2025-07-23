import random
import string
from typing import List


def generate_random_email(domain: str = "mailsac.com") -> str:
    """Generate a random email address.
    
    Args:
        domain: The domain to use (default: mailsac.com)
        
    Returns:
        A randomly generated email address
    """
    # Generate random username with letters and numbers
    username_length = random.randint(8, 12)
    username = ''.join(random.choices(
        string.ascii_lowercase + string.digits,
        k=username_length
    ))
    
    return f"{username}@{domain}"


def format_timestamp(timestamp: str) -> str:
    """Format a timestamp for display.
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        Formatted timestamp string
    """
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return timestamp


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to a maximum length.
    
    Args:
        text: The text to truncate
        max_length: Maximum length (default: 50)
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def extract_plain_text(html_content: str) -> str:
    """Extract plain text from HTML content.
    
    Args:
        html_content: HTML content string
        
    Returns:
        Plain text content
    """
    try:
        from html import unescape
        import re
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        # Unescape HTML entities
        text = unescape(text)
        # Clean up whitespace
        text = ' '.join(text.split())
        
        return text
    except Exception:
        return html_content