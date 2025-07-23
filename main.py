#!/usr/bin/env python3
"""
Temporary Email Service
A CLI application for managing temporary emails using Mailsac API with AI features powered by Gemini.
"""

from app import TempEmailApp

def main():
    """Main entry point for the application."""
    app = TempEmailApp()
    app.run()

if __name__ == "__main__":
    main()