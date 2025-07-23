"""
Application constants and configuration values
"""

from enum import Enum


class BotMessages:
    """Bot response messages."""
    
    # Welcome and help messages
    WELCOME_MESSAGE = """
🤖 **Welcome to Advanced Temp Email Bot!**

🚀 **Features:**
• 📧 Generate temporary emails instantly
• 🤖 AI-powered email analysis with Gemini
• 📬 Real-time inbox monitoring
• 🔒 Privacy-first approach

🎯 **Quick Actions:**
Use the buttons below or try these commands:
• `/new_email` - Create new temp email
• `/inbox` - View current inbox
• `/help` - Show all commands
    """
    
    HELP_MESSAGE = """
🤖 **Advanced Temp Email Bot - Commands**

📧 **Email Management:**
• `/start` - Show welcome message and main menu
• `/new_email` - Generate new temporary email
• `/inbox` - View current inbox
• `/read <id>` - Read specific email
• `/delete <id>` - Delete specific email
• `/clear` - Clear all emails

🤖 **AI Features:**
• `/summarize <id>` - Get AI summary of email
• `/ask <id> <question>` - Ask AI about email content
• `/analyze <id>` - Analyze email for spam/phishing

⚙️ **Settings:**
• `/settings` - Configure bot preferences
• `/stats` - View usage statistics

❓ **Need Help?**
Contact support or check our documentation for more details.
    """
    
    # Success messages
    EMAIL_CREATED = """
📧 **New Temporary Email Created!**

`{email_address}`

🔄 This email is ready to receive messages
📬 Use `/inbox` to check for new emails
⏱️ Emails auto-delete after 24 hours

💡 **Pro tip:** You can use AI to analyze emails!
    """
    
    INBOX_EMPTY = "📭 Your inbox is empty!"
    INBOX_HEADER = "📬 **Inbox for** `{email_address}`\n\n"
    SETTINGS_COMING_SOON = "⚙️ Settings panel coming soon!"
    
    # Error messages
    ERROR_GENERIC = "❌ Something went wrong. Please try again."
    ERROR_EMAIL_CREATION = "❌ Failed to create new email. Please try again."
    ERROR_INBOX_FETCH = "❌ Failed to fetch inbox. Please try again."
    ERROR_EMAIL_NOT_FOUND = "❌ Email not found. Please check the email ID."
    ERROR_INVALID_COMMAND = "❌ Invalid command. Type '/help' for available commands."
    ERROR_API_UNAVAILABLE = "❌ Service temporarily unavailable. Please try again later."
    ERROR_RATE_LIMIT = "❌ Too many requests. Please wait a moment before trying again."
    
    # AI messages
    AI_THINKING = "🤖 AI is analyzing..."
    AI_SUMMARIZING = "📝 AI is summarizing the message..."
    AI_SECURITY_CHECK = "🛡️ AI is checking email security..."
    AI_ERROR = "❌ AI service is temporarily unavailable."


class APIConstants:
    """API-related constants."""
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 60
    MAX_REQUESTS_PER_HOUR = 1000
    
    # Timeouts (seconds)
    HTTP_TIMEOUT = 30
    API_TIMEOUT = 15
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_BACKOFF = 2
    
    # Cache settings
    CACHE_TTL_SECONDS = 300  # 5 minutes
    MAX_CACHE_SIZE = 1000


class EmailConstants:
    """Email-related constants."""
    
    # Email validation
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    MAX_EMAIL_LENGTH = 254
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 64
    
    # Default settings
    DEFAULT_DOMAIN = "mailsac.com"
    DEFAULT_RETENTION_HOURS = 24
    MAX_EMAILS_PER_USER = 10
    
    # Content limits
    MAX_SUBJECT_LENGTH = 200
    MAX_BODY_LENGTH = 50000
    MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10MB


class LogConstants:
    """Logging constants."""
    
    # Log levels
    DEFAULT_LOG_LEVEL = "INFO"
    
    # Log formats
    STANDARD_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DETAILED_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    
    # Log messages
    USER_ACTION = "User {user_id} performed action: {action}"
    API_REQUEST = "API request to {service}: {method} {endpoint}"
    API_ERROR = "API error from {service}: {status_code} - {error}"
    CACHE_HIT = "Cache hit for key: {key}"
    CACHE_MISS = "Cache miss for key: {key}"


class SecurityConstants:
    """Security-related constants."""
    
    # Input sanitization
    ALLOWED_CHARS = r'[a-zA-Z0-9\s\-_.@]'
    MAX_INPUT_LENGTH = 1000
    
    # Rate limiting
    USER_RATE_LIMIT = 30  # requests per minute per user
    GLOBAL_RATE_LIMIT = 1000  # requests per minute globally
    
    # Content filtering
    BLOCKED_PATTERNS = [
        r'<script.*?>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe.*?>.*?</iframe>',
    ]


class StatusCode(Enum):
    """HTTP status code constants."""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503