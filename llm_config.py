"""
LLM Configuration File
Modify all LLM-related parameters here
"""
import os

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")

# Primary API Provider (groq/openai)
PRIMARY_API = "groq"  # Options: "groq" or "openai"

# Model Configuration
MODEL_NAME = "openai/gpt-oss-120b"  # Default model name
MAX_TOKENS = 2000  # Maximum tokens to generate
TEMPERATURE = 0.7  # Temperature for generation
GROQ_MODELS = {
    "default": "openai/gpt-oss-120b",
    "fast": "llama-3.1-8b-instant",
    "powerful": "llama-3.1-70b-versatile"
}

OPENAI_MODELS = {
    "default": "gpt-4o-mini",
    "fast": "gpt-3.5-turbo",
    "powerful": "gpt-4o"
}

# Generation Parameters
DEFAULT_MAX_TOKENS = 2000
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 1.0

# Chat Configuration
MAX_CONVERSATION_HISTORY = 10
SYSTEM_MESSAGE_ENABLED = True

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Debug Configuration
DEBUG_MODE = False
LOG_API_CALLS = False

class QAParameters:
    """Q&A system specific parameters"""
    
    # Response Parameters
    MAX_RESPONSE_LENGTH = 2000
    MIN_RESPONSE_LENGTH = 50
    
    # Conversation Flow
    ENABLE_STEP_BY_STEP = True
    MAX_QUESTIONS_PER_TURN = 1
    
    # Personalization
    ENABLE_NAME_USAGE = True
    ENABLE_AGE_BASED_BRANCHING = True
    
    # Content Filtering
    ENABLE_CONTENT_FILTER = True
    FORBIDDEN_TOPICS = []
    
    # Language Settings
    PRIMARY_LANGUAGE = "en"
    ALLOW_MULTILINGUAL = True
