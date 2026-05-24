import logging
from typing import Optional
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application configuration from environment variables"""
    
    # API Configuration
    API_TITLE: str = "BugPulse API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # External API Configuration
    EXTERNAL_API_URL: str = "https://api.example.com/bugs"
    EXTERNAL_API_KEY: str = ""
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./bugs.db"
    
    # Google Chat Configuration
    GOOGLE_CHAT_WEBHOOK_URL: str = ""
    
    # Scheduler Configuration
    SCHEDULER_INTERVAL: int = 5  # minutes
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
