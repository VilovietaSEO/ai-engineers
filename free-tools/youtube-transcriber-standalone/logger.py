"""
Logging configuration using loguru
"""
import sys
from pathlib import Path
from loguru import logger
import os
import time
from contextlib import contextmanager

# Remove default logger
logger.remove()

# Get settings from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "false").lower() == "true"
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log")

# Console format with colors
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# Console handler
logger.add(
    sys.stdout,
    format=log_format,
    level=LOG_LEVEL,
    colorize=True
)

# File handler (if enabled)
if LOG_TO_FILE:
    Path(LOG_FILE_PATH).parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        LOG_FILE_PATH,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention=5,
        compression="zip"
    )


@contextmanager
def log_timer(operation: str, **kwargs):
    """Context manager to time operations"""
    start = time.time()
    logger.info(f"Starting: {operation}", **kwargs)
    try:
        yield
        duration = time.time() - start
        logger.info(f"Completed: {operation} ({duration:.2f}s)", duration=duration, **kwargs)
    except Exception as e:
        duration = time.time() - start
        logger.error(f"Failed: {operation} ({duration:.2f}s)", duration=duration, error=str(e), **kwargs)
        raise


def get_logger(name: str):
    """Get a logger with a specific name/module context"""
    return logger.bind(module=name)


__all__ = ['logger', 'get_logger', 'log_timer']
