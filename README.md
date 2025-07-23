# 🤖 Advanced Telegram Temp Email Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-blue.svg)](https://core.telegram.org/bots/api)
[![Mailsac API](https://img.shields.io/badge/Mailsac-API-green.svg)](https://mailsac.com)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🚀 **Next-generation temporary email bot** powered by AI intelligence, offering seamless temporary email management with advanced features through Telegram.

## 🌟 Features

### 🎯 Core Functionality
- **🔥 Instant Email Generation** - Create temporary emails in seconds
- **📬 Real-time Inbox Management** - Monitor emails as they arrive
- **🤖 AI-Powered Email Analysis** - Gemini AI integration for smart email processing
- **🗑️ Auto-cleanup** - Automatic email deletion with customizable retention
- **🔒 Privacy-First** - No data storage, all interactions are ephemeral

### 🧠 AI-Enhanced Features
- **📝 Smart Email Summarization** - Get AI-generated summaries of long emails
- **❓ Intelligent Q&A** - Ask questions about email content
- **🔍 Content Analysis** - Detect spam, phishing, and important emails
- **🌐 Multi-language Support** - AI translations and responses
- **📊 Email Insights** - Analysis of sender patterns and content themes

### ⚡ Advanced Capabilities
- **🔄 Real-time Updates** - WebSocket integration for instant notifications
- **📎 Attachment Handling** - Download and preview email attachments
- **🎨 Rich UI/UX** - Interactive inline keyboards and formatted responses
- **⚙️ Customizable Settings** - User preferences and notification controls
- **📈 Analytics Dashboard** - Email statistics and usage insights

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Bot Framework** | [aiogram 3.x](https://aiogram.dev/) | Modern async Telegram bot framework |
| **Email API** | [Mailsac API](https://mailsac.com/) | Temporary email service provider |
| **AI Engine** | [Google Gemini](https://ai.google.dev/) | Advanced language model for email analysis |
| **HTTP Client** | [aiohttp](https://docs.aiohttp.org/) | Async HTTP requests |
| **Data Validation** | [Pydantic](https://pydantic.dev/) | Type validation and settings management |
| **Logging** | [Rich](https://rich.readthedocs.io/) | Beautiful console output and logging |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed
- Telegram Bot Token from [@BotFather](https://t.me/botfather)
- [Mailsac API Key](https://mailsac.com/api-keys) (Free tier available)
- [Google AI API Key](https://makersuite.google.com/app/apikey) for Gemini

### 1️⃣ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/telegram-temp-email-bot.git
cd telegram-temp-email-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configuration

Create a `.env` file in the project root:

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Mailsac Configuration
MAILSAC_API_KEY=your_mailsac_api_key_here
MAILSAC_BASE_URL=https://mailsac.com/api

# Google Gemini Configuration
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
GEMINI_MODEL=gemini-pro

# Bot Configuration (Optional)
BOT_USERNAME=your_bot_username
WEBHOOK_URL=your_webhook_url  # For production
DEBUG=false
LOG_LEVEL=INFO

# Email Configuration (Optional)
DEFAULT_EMAIL_DOMAIN=mailsac.com
EMAIL_RETENTION_HOURS=24
MAX_EMAILS_PER_USER=10
```

### 3️⃣ Running the Bot

```bash
# Development mode
python main.py

# Production mode with webhook
python main.py --webhook
```

## 📋 API Endpoints & Commands

### 🎮 Bot Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize bot and show welcome | `/start` |
| `/new_email` | Generate new temporary email | `/new_email` |
| `/inbox` | View current inbox | `/inbox` |
| `/read <id>` | Read specific email | `/read 12345` |
| `/summarize <id>` | AI summary of email | `/summarize 12345` |
| `/ask <id> <question>` | Ask AI about email | `/ask 12345 "Is this spam?"` |
| `/delete <id>` | Delete specific email | `/delete 12345` |
| `/clear` | Clear all emails | `/clear` |
| `/settings` | Bot configuration | `/settings` |
| `/help` | Show help message | `/help` |

### 🔧 Inline Actions

- **📧 Quick Actions**: Reply, Forward, Archive
- **🤖 AI Features**: Summarize, Translate, Analyze
- **⚙️ Settings**: Notifications, Auto-delete, Language
- **📊 Analytics**: View stats, Export data

## 🏗️ Project Structure

```
telegram-temp-email-bot/
├── 📁 src/
│   ├── 📁 bot/
│   │   ├── handlers/          # Message and callback handlers
│   │   ├── keyboards/         # Inline keyboard layouts
│   │   ├── middleware/        # Bot middleware components
│   │   └── utils/            # Bot utility functions
│   ├── 📁 services/
│   │   ├── mailsac.py        # Mailsac API client
│   │   ├── gemini.py         # Google Gemini AI client
│   │   └── email_processor.py # Email processing logic
│   ├── 📁 models/
│   │   ├── email.py          # Email data models
│   │   └── user.py           # User settings models
│   └── 📁 config/
│       ├── settings.py       # Application settings
│       └── logging.py        # Logging configuration
├── 📁 tests/                 # Unit and integration tests
├── 📁 docs/                  # Additional documentation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── main.py                  # Application entry point
└── README.md               # This documentation
```

## 🔌 API Integration Details

### Mailsac API Integration

```python
# Example API calls
GET /api/addresses/{email}/messages     # List messages
GET /api/text/{email}/{messageId}       # Get message content
DELETE /api/addresses/{email}/messages/{messageId}  # Delete message
```

### Gemini AI Integration

```python
# AI-powered features
- Email summarization with context awareness
- Spam/phishing detection using pattern analysis  
- Intelligent content extraction and categorization
- Multi-language support for global users
```

## 🚀 Advanced Features

### 🤖 AI Capabilities

#### Smart Email Analysis
```python
# Automatic categorization
categories = ["spam", "promotional", "personal", "business", "verification"]

# Sentiment analysis
sentiment = gemini.analyze_sentiment(email_content)

# Security assessment  
security_score = gemini.assess_email_security(email_content)
```

#### Intelligent Responses
```python
# Context-aware Q&A
user_question = "Is this email safe to click?"
ai_response = gemini.analyze_email_safety(email_content, user_question)

# Multi-language support
translated_content = gemini.translate_email(email_content, target_language="es")
```

### 📊 Analytics & Monitoring

- **📈 Usage Statistics**: Track bot usage patterns
- **🔍 Email Analysis**: Categorize and analyze email types  
- **⚡ Performance Metrics**: Response times and API health
- **🛡️ Security Monitoring**: Detect suspicious activities

### 🔒 Security Features

- **🚫 No Data Persistence**: All data is ephemeral
- **🔐 API Key Encryption**: Secure credential management
- **🛡️ Input Validation**: Prevent injection attacks
- **📝 Audit Logging**: Track all bot interactions

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/e2e/          # End-to-end tests

# Generate coverage report
pytest --cov=src --cov-report=html
```

## 🚀 Deployment

### 🐳 Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py", "--webhook"]
```

```bash
# Build and run
docker build -t temp-email-bot .
docker run -d --env-file .env temp-email-bot
```

### ☁️ Cloud Deployment Options

- **🚀 Heroku**: One-click deployment with Procfile
- **🌐 Railway**: Modern cloud platform with easy setup
- **⚡ Vercel**: Serverless deployment for webhook mode
- **🔧 VPS**: Traditional server deployment with systemd

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **🍴 Fork** the repository
2. **🌿 Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **✨ Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **📤 Push** to the branch (`git push origin feature/amazing-feature`)
5. **🔃 Open** a Pull Request

### 📝 Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints for all functions
- Write comprehensive tests for new features
- Update documentation for API changes
- Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Telegram Bot API](https://core.telegram.org/bots/api)** - Powerful bot platform
- **[Mailsac](https://mailsac.com/)** - Reliable temporary email service
- **[Google Gemini](https://ai.google.dev/)** - Advanced AI capabilities
- **[aiogram](https://aiogram.dev/)** - Modern Python Telegram bot framework

## 📞 Support

- **📖 Documentation**: [Wiki](https://github.com/yourusername/telegram-temp-email-bot/wiki)
- **🐛 Bug Reports**: [Issues](https://github.com/yourusername/telegram-temp-email-bot/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/yourusername/telegram-temp-email-bot/discussions)
- **📧 Email**: support@yourproject.com
---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ by developers, for developers

[🚀 Get Started](#-quick-start) • [📖 Documentation](docs/) • [🤝 Contribute](#-contributing)

</div>
