# Temporary Email Service

A command-line application for managing temporary emails using the Mailsac API with AI-powered features via Google's Gemini.

## Features

- 📧 **Temporary Email Management**: Create and manage temporary email addresses
- 🔍 **Inbox Viewing**: List all emails with sender, subject, and timestamp
- 📖 **Email Reading**: Read full email content with clean formatting
- 🤖 **AI Summarization**: Get AI-powered summaries of email content
- ❓ **AI Q&A**: Ask specific questions about email content
- 🗑️ **Email Deletion**: Delete unwanted emails
- 🎨 **Rich CLI Interface**: Beautiful command-line interface with colors and formatting

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys** in `.env` file:
   ```
   MAILSAC_API_KEY=your_mailsac_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Get your API keys from:
   - Mailsac: https://mailsac.com/api-keys
   - Gemini: https://makersuite.google.com/app/apikey

## Usage

Run the application:
```bash
python main.py
```

### Available Commands

- `inbox` - View all emails in your inbox
- `read <message_id>` - Read a specific email
- `summarize <message_id>` - Get AI summary of an email
- `ask <message_id> "<question>"` - Ask AI about email content
- `delete <message_id>` - Delete an email
- `new_address` - Switch to a different email address
- `help` - Show help message
- `exit` - Exit the application

### Example Usage

1. **Start the application and generate an email**:
   ```
   python main.py
   ```

2. **View your inbox**:
   ```
   > inbox
   ```

3. **Read an email**:
   ```
   > read 1234567890
   ```

4. **Summarize an email**:
   ```
   > summarize 1234567890
   ```

5. **Ask about an email**:
   ```
   > ask 1234567890 "What is the main topic of this email?"
   ```

## Project Structure

```
├── main.py           # Entry point
├── app.py            # Main application logic and CLI
├── mailsac.py        # Mailsac API client
├── gemini.py         # Gemini AI client
├── utils.py          # Utility functions
├── requirements.txt  # Python dependencies
└── .env             # API keys (create this file)
```

## Dependencies

- `requests` - HTTP client for Mailsac API
- `rich` - Rich text and beautiful formatting in terminal
- `google-generativeai` - Gemini AI client
- `python-dotenv` - Environment variable management

## API Documentation

### Mailsac API
- Documentation: https://mailsac.com/docs/api
- Free tier available with rate limits

### Gemini API  
- Documentation: https://ai.google.dev/docs
- Free tier available with generous limits

## Error Handling

The application includes comprehensive error handling for:
- Invalid API keys
- Network connectivity issues
- Invalid message IDs
- API rate limits
- Malformed responses

## Security Notes

- Never commit your `.env` file with real API keys
- API keys are loaded from environment variables
- No sensitive data is logged or stored locally

## License

This project is for educational purposes. Please check the terms of service for Mailsac and Gemini APIs when using in production.