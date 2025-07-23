# Lego Toolkit: Gemini-Powered Telegram Bot

## Overview
A blazing-fast, clean-architecture Telegram bot powered by Google Gemini AI ("gemini-pro"), built with aiogram v3+ for elite async performance, robust config, and beautiful inline UX.

---

## Features

- **/start** — Greet users and show options
- **/ask** — Ask anything directly to Gemini
- **Inline**: "💬 Chat with Gemini" button for instant AI chat
- **Auto-reply** for unrecognized messages
- **Gemini AI Integration**: Human-like, creative, and helpful responses
- **Clean, maintainable codebase** (Clean Architecture)
- **Async, fast, and secure** (aiogram v3+)
- **Easy config lockdown**
- **Extensible**: Ready for reminders, summaries, document parsing, etc.

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/lego-toolkit.git
cd lego-toolkit
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `config.py` file or set environment variables:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `GOOGLE_API_KEY`: Your Google Generative AI API key

### 4. Run the bot
```bash
python bot.py
```

---

## Usage
- Start the bot with `/start`.
- Use `/ask` to ask Gemini anything.
- Tap "💬 Chat with Gemini" for inline chat.
- Any other message gets an AI reply.

---

## File Structure
- `bot.py` — Main bot logic and entry point
- `config.py` — Configuration and secrets
- `requirements.txt` — Python dependencies

---

## Extending
- Add new features in a modular way (see `core/` and `services/` if you expand)
- Ready for task automation, reminders, summaries, etc.

---

## License
MIT 