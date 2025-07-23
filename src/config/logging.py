"""
Logging configuration
"""

import logging
import sys
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install


def setup_logging(log_level: str = "INFO", debug: bool = False) -> None:
    """Setup application logging with Rich formatting."""
    
    # Install Rich traceback handler
    install(show_locals=debug)
    
    # Create console for Rich handler
    console = Console(stderr=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=debug,
                markup=True
            )
        ]
    )
    
    # Set specific logger levels
    loggers_config = {
        "aiogram": "WARNING" if not debug else "DEBUG",
        "aiohttp": "WARNING" if not debug else "INFO",
        "google.generativeai": "WARNING" if not debug else "INFO",
    }
    
    for logger_name, level in loggers_config.items():
        logging.getLogger(logger_name).setLevel(getattr(logging, level))
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 Logging configured - Level: {log_level}, Debug: {debug}")