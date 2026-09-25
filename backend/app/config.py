"""
Configuration management.
Unified configuration loaded from project root .env file.
"""

import os
from dotenv import load_dotenv

# Load project root .env file
# Path: synthetic-minds/.env (relative to backend/app/config.py)
project_root_env = os.path.join(os.path.dirname(__file__), '../../.env')

if os.path.exists(project_root_env):
    load_dotenv(project_root_env, override=True)
else:
    # If no .env at root, load environment variables (for production / containerized environments)
    load_dotenv(override=True)


class Config:
    """Flask configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'synthetic-minds-secret-key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # JSON settings - disable ASCII escaping for clean UTF-8
    JSON_AS_ASCII = False
    
    # OpenAI LLM settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or os.environ.get('LLM_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL') or os.environ.get('LLM_MODEL_NAME', 'gpt-4o-mini')
    
    # Internal compatibility aliases
    LLM_API_KEY = OPENAI_API_KEY
    LLM_MODEL_NAME = OPENAI_MODEL
    LLM_BASE_URL = os.environ.get('LLM_BASE_URL', 'https://api.openai.com/v1')
    
    # Zep configuration
    ZEP_API_KEY = os.environ.get('ZEP_API_KEY')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    if os.environ.get('VERCEL'):
        UPLOAD_FOLDER = '/tmp/uploads'
        OASIS_SIMULATION_DATA_DIR = '/tmp/uploads/simulations'
    else:
        UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
        OASIS_SIMULATION_DATA_DIR = os.path.join(os.path.dirname(__file__), '../uploads/simulations')
    ALLOWED_EXTENSIONS = {'pdf', 'md', 'txt', 'markdown'}
    
    # Text processing settings
    DEFAULT_CHUNK_SIZE = 500  # Default chunk size
    DEFAULT_CHUNK_OVERLAP = 50  # Default overlap size
    
    # OASIS simulation settings
    OASIS_DEFAULT_MAX_ROUNDS = int(os.environ.get('OASIS_DEFAULT_MAX_ROUNDS', '10'))
    
    # OASIS platform available actions
    OASIS_TWITTER_ACTIONS = [
        'CREATE_POST', 'LIKE_POST', 'REPOST', 'FOLLOW', 'DO_NOTHING', 'QUOTE_POST'
    ]
    OASIS_REDDIT_ACTIONS = [
        'LIKE_POST', 'DISLIKE_POST', 'CREATE_POST', 'CREATE_COMMENT',
        'LIKE_COMMENT', 'DISLIKE_COMMENT', 'SEARCH_POSTS', 'SEARCH_USER',
        'TREND', 'REFRESH', 'DO_NOTHING', 'FOLLOW', 'MUTE'
    ]
    
    # Report Agent settings
    REPORT_AGENT_MAX_TOOL_CALLS = int(os.environ.get('REPORT_AGENT_MAX_TOOL_CALLS', '5'))
    REPORT_AGENT_MAX_REFLECTION_ROUNDS = int(os.environ.get('REPORT_AGENT_MAX_REFLECTION_ROUNDS', '2'))
    REPORT_AGENT_TEMPERATURE = float(os.environ.get('REPORT_AGENT_TEMPERATURE', '0.5'))
    
    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration values."""
        errors: list[str] = []
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is not configured")
        if not cls.ZEP_API_KEY:
            errors.append("ZEP_API_KEY is not configured")
        if os.environ.get("ZEP_API_URL"):
            errors.append("ZEP_API_URL is not supported; Synthetic Minds connects exclusively to Zep Cloud")
        if cls.DEBUG:
            import warnings
            warnings.warn("Flask DEBUG mode is enabled. Do not use in production.", RuntimeWarning)
        return errors
