import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

# Google Gemini AI configuration  
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Bot settings
MAX_MESSAGE_LENGTH = 4096  # Telegram message length limit
RATE_LIMIT = 1  # Messages per second per user
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]  # Admin user IDs

# Gemini settings
TEMPERATURE = 0.7  # Controls randomness (0.0-1.0)
TOP_P = 0.8  # Controls diversity of responses
TOP_K = 40  # Controls vocabulary range

# Error messages
ERROR_MESSAGES = {
    "rate_limit": "Please wait a moment before sending another message.",
    "api_error": "Sorry, I encountered an error. Please try again later.",
    "invalid_input": "Please provide a valid input.",
}