"""
Logging Configuration Module.
Provides centralized logging to both console and rotating log files.
"""

import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler


def _ensure_utf8_stdout():
    """Ensure standard stdout and stderr streams use UTF-8 encoding."""
    if sys.platform == 'win32':
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')


# Log directory path
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')


def setup_logger(name: str = 'synthetic_minds', level: int = logging.DEBUG) -> logging.Logger:
    """
    Configure and initialize application logger.
    
    Args:
        name: Logger namespace name
        level: Minimum logging level
        
    Returns:
        Configured logging.Logger instance
    """
    # Ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Create or retrieve logger
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(level)
    
    # Prevent duplicate outputs to root logger
    logger_instance.propagate = False
    
    # If handlers already configured, return existing instance
    if logger_instance.handlers:
        return logger_instance
    
    # Log format definitions
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # 1. Rotating File Handler - Detailed logs
    log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, log_filename),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # 2. Console Handler - Clean logs for INFO and above
    _ensure_utf8_stdout()
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Attach handlers
    logger_instance.addHandler(file_handler)
    logger_instance.addHandler(console_handler)
    
    return logger_instance


def get_logger(name: str = 'synthetic_minds') -> logging.Logger:
    """
    Retrieve or create a logger by name.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    logger_instance = logging.getLogger(name)
    if not logger_instance.handlers:
        return setup_logger(name)
    return logger_instance


# Initialize default logger
logger = setup_logger()


# Convenience methods
def debug(msg: str, *args, **kwargs) -> None:
    logger.debug(msg, *args, **kwargs)

def info(msg: str, *args, **kwargs) -> None:
    logger.info(msg, *args, **kwargs)

def warning(msg: str, *args, **kwargs) -> None:
    logger.warning(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs) -> None:
    logger.error(msg, *args, **kwargs)

def critical(msg: str, *args, **kwargs) -> None:
    logger.critical(msg, *args, **kwargs)
