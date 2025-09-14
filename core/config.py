"""
Application Configuration
"""
import os
from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application Configuration"""
    
    # Groq API Configuration
    groq_api_key: str = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
    default_model: str = "openai/gpt-oss-120b"
    max_tokens: int = 1024
    temperature: float = 0.7
    
    # Database Configuration
    vector_db_path: str = "data/vector_db"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Chat Configuration
    max_conversation_turns: int = 10
    conversation_memory_window: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global configuration instance
settings = Settings()
